"""
Script de extração de entidades de comentários de avaliações.

Este script usa um modelo de linguagem (GPT-4o) para extrair entidades
relevantes dos comentários, como problemas técnicos, funcionalidades
com falhas, e outros elementos mencionados nas avaliações.

Utiliza técnica de reflexão para melhorar a qualidade da extração,
revisando o resultado inicial para recuperar entidades que possam
ter sido perdidas na primeira passada.
"""

from openai import OpenAI
import json
from typing import List, Dict, Optional
from datetime import datetime
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Modelo GPT a ser usado para extração de entidades
# Pode ser alterado via variável de ambiente OPENAI_MODEL
# Por padrão usa gpt-4o-mini (mais rápido e econômico)
MODEL_NAME = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

# Tipos de entidades esperadas para o domínio bancário
ENTITY_TYPES = [
    "Issue",    # Problemas técnicos ou funcionais mencionados (todos os comentários negativos)
    "App",      # Aplicativo mencionado
    "User",     # Usuário/autor do comentário
    "Service",  # Serviços bancários
    "Device",   # Dispositivo/plataforma
]

ENTITY_EXTRACTION_SYSTEM = """Você é um assistente de IA que extrai entidades de comentários sobre aplicativos bancários. Sempre responda em formato JSON.

<TIPOS_DE_ENTIDADES>
Abaixo estão os tipos de entidades esperadas no grafo de conhecimento.
Se você extrair uma entidade que se encaixa em um desses tipos, atribua esse label.
Se não, você pode criar um novo label ou atribuir um array vazio.

Tipos de entidades:
- Issue: Problemas técnicos ou funcionais mencionados (ex: "PIX não funciona", "Não consigo fazer login", "App trava", "Lentidão", "Biometria não funciona")
- App: Aplicativo mencionado (ex: Santander, Bradesco)
- User: Usuário/autor do comentário
- Service: Serviços bancários (ex: Empréstimos, Investimentos)
- Device: Dispositivo ou plataforma (ex: Android, iOS)

IMPORTANTE: Como estamos processando comentários NEGATIVOS (avaliações de 1-2 estrelas), TODAS as entidades extraídas devem ser classificadas como Issue. Não há necessidade de distinguir entre funcionalidades positivas e problemas - tudo é problema.
</TIPOS_DE_ENTIDADES>

<DIRETRIZES_DE_EXTRAÇÃO>
1. Extraia TODAS as entidades significativas mencionadas explicitamente ou implicitamente
2. Use o nome completo e não abreviado para entidades
3. Inclua entidades referenciadas por pronomes se identificáveis pelo contexto
4. Crie um resumo breve (<250 palavras) para cada entidade
5. NÃO extraia:
   - Nome do aplicativo mencionado no contexto (já temos como metadado)
   - Palavras genéricas como "aplicativo", "app", "aplicativo Santander" (todos comentários são sobre o app)
   - Versão do app mencionada no contexto (já temos como metadado)
   - Relacionamentos (isso vem depois)
   - Informações temporais (tratadas separadamente)
   - Ações ou verbos isolados
   - Issues muito genéricas sem contexto específico: "Erro", "Problema", "Dificuldade", "Confusão", "Decepção", "Expectativa", "Mudança", "Identificação", "Dependência"
   - Issues não relacionadas ao app: "Cartão Não Chegou" (entrega física), "Cliente de Longa Data" (característica do cliente), "Assinatura", "Avaliação", "Sorteio", "Recompensa", "Fatura Fechada"
   - Características do cliente: "Cliente", "Usuário", "Pessoa" (não são problemas do app)
6. Foque em entidades que representam problemas ESPECÍFICOS (Issues) mencionados relacionados ao FUNCIONAMENTO DO APP
7. NÃO inclua o nome do app ou versão nas entidades extraídas
8. TODAS as entidades extraídas devem ter o label "Issue"
9. IMPORTANTE: Só extraia Issues que possam ser relacionadas a funcionalidades do app (ex: "Erro ao fazer PIX" é válido, mas "Erro" isolado não é)

<DISTINÇÃO_ABERTURA_APP_VS_ABERTURA_CONTA>
CRÍTICO: Distinguir entre dois tipos de "abertura" (ambos são Issues, mas mapeiam para BusinessCapabilities diferentes):
- "Não abre" / "App não abre" / "Não consegue abrir o app" → Issue relacionado a Performance (app não inicia)
- "Não consigo abrir conta" / "Não dá pra abrir conta" / "Problemas para abrir conta" → Issue relacionado a Cadastro/Conta (processo de abertura de conta bancária)

Use o contexto para identificar:
- Se menciona "abrir conta", "abrir conta bancária", "cadastrar conta" → Cadastro/Conta
- Se menciona apenas "não abre", "app não abre", "não abre o aplicativo" → Performance
</DISTINÇÃO_ABERTURA_APP_VS_ABERTURA_CONTA>

<EXEMPLOS_DE_ENTIDADES_VÁLIDAS>
Issue: "Lentidão", "Não reconhece biometria", "Problemas de Abertura do App", "Problemas de Abertura de Conta", "Falta de Confiança", "Erro ao fazer PIX", "Acesso a Saldo", "Refinanciamento", "Chat de Suporte", "Atualização de Dados", "Transparência", "Espionagem", "Tarifas"
</EXEMPLOS_DE_ENTIDADES_VÁLIDAS>

<EXEMPLOS_DE_ENTIDADES_INVÁLIDAS>
NÃO extraia:
- "Aplicativo", "App", "Santander" (nome do app), "25.9.1.3" (versão)
- "Usuário", "Cliente", "Pessoa" (características do cliente, não problemas do app)
- "Erro", "Problema", "Dificuldade" (muito genéricas sem contexto específico)
- "Cartão Não Chegou" (entrega física, não funcionalidade do app)
- "Cliente de Longa Data" (característica do cliente, não problema do app)
- "Assinatura", "Avaliação", "Sorteio", "Recompensa" (não relacionadas ao app)
- "Decepção", "Expectativa", "Confusão" (sentimentos genéricos sem contexto específico)
</EXEMPLOS_DE_ENTIDADES_INVÁLIDAS>
</DIRETRIZES_DE_EXTRAÇÃO>
"""

ENTITY_EXTRACTION_USER = """<COMENTÁRIO>
{review_content}
</COMENTÁRIO>

<CONTEXTO_ADICIONAL>
App: {app_name}
Data: {review_date}
Versão: {review_version}
</CONTEXTO_ADICIONAL>

Extraia todas as entidades do COMENTÁRIO. Como este é um comentário negativo, TODAS as entidades extraídas devem ser classificadas como Issue.

ATENÇÃO ESPECIAL:
1. TODAS as entidades extraídas devem ter o label "Issue"
2. Se menciona "não abre conta" ou "abrir conta", extraia como Issue relacionado a Cadastro/Conta
3. Se menciona apenas "não abre" (sem "conta"), extraia como Issue relacionado a Performance
4. Foque em problemas, dificuldades, funcionalidades que não funcionam, ou aspectos negativos mencionados

IMPORTANTE: Responda APENAS com JSON válido, sem texto adicional.

Formato JSON esperado:
{{
  "extracted_entities": [
    {{
      "name": "Nome da Entidade",
      "labels": ["Issue"],
      "summary": "Breve descrição da entidade e o que sabemos sobre ela"
    }}
  ]
}}
"""

REFLECTION_PROMPT = """<EXTRACTED_ENTITIES>
{already_extracted}
</EXTRACTED_ENTITIES>

<ORIGINAL_EPISODE>
{review_content}
</ORIGINAL_EPISODE>

Revise o episódio novamente. Há alguma entidade que foi perdida?
Procure por:
- Entidades implícitas (referenciadas mas não nomeadas diretamente)
- Entidades mencionadas por pronomes
- Entidades de fundo assumidas mas não declaradas
- Problemas ou dificuldades mencionados indiretamente

IMPORTANTE: 
- Responda APENAS com JSON válido, sem texto adicional.
- TODAS as entidades devem ter o label "Issue"

Retorne apenas NOVAS entidades não presentes em EXTRACTED_ENTITIES, ou array vazio se completo.

Formato JSON esperado:
{{
  "extracted_entities": [
    {{
      "name": "Nome da Entidade",
      "labels": ["Issue"],
      "summary": "Breve descrição"
    }}
  ]
}}
"""


class EntityExtractor:
    """
    Extrator de entidades usando modelo de linguagem.
    
    Utiliza técnica de reflexão para melhorar a qualidade da extração:
    faz uma primeira passada para extrair entidades e depois revisa
    o resultado para recuperar entidades que possam ter sido perdidas.
    """
    
    def __init__(self, client: Optional[OpenAI] = None):
        self.client = client or OpenAI()
        self.model = MODEL_NAME
    
    def extract_entities(self, review_content: str, app_name: str = "", 
                        review_date: str = "", review_version: str = "") -> List[Dict]:
        """
        Extrai entidades de um comentário de avaliação.
        
        Args:
            review_content: Texto do comentário
            app_name: Nome do aplicativo
            review_date: Data da avaliação
            review_version: Versão do app mencionada
            
        Returns:
            Lista de entidades extraídas com name, labels, summary
        """
        # Primeira passada: extração inicial de entidades
        prompt = ENTITY_EXTRACTION_USER.format(
            review_content=review_content,
            app_name=app_name or "N/A",
            review_date=review_date or "N/A",
            review_version=review_version or "N/A"
        )
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": ENTITY_EXTRACTION_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        result = json.loads(response.choices[0].message.content)
        extracted_entities = result.get("extracted_entities", [])
        
        # Segunda passada: reflexão para recuperar entidades perdidas
        # A técnica de reflexão ajuda a recuperar entidades que podem ter
        # sido perdidas na primeira passada, melhorando a qualidade da extração
        reflection_prompt = REFLECTION_PROMPT.format(
            already_extracted=json.dumps(extracted_entities, ensure_ascii=False, indent=2),
            review_content=review_content
        )
        
        reflection_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Você é um assistente que identifica entidades perdidas em extrações. Sempre responda em formato JSON."},
                {"role": "user", "content": reflection_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        reflection_result = json.loads(reflection_response.choices[0].message.content)
        additional_entities = reflection_result.get("extracted_entities", [])
        
        # Combina os resultados das duas passadas
        all_entities = extracted_entities + additional_entities
        
        # Remove duplicatas por nome (case-insensitive)
        # Pode acontecer de a mesma entidade ser extraída nas duas passadas
        seen_names = set()
        unique_entities = []
        for entity in all_entities:
            name_lower = entity.get("name", "").lower()
            if name_lower and name_lower not in seen_names:
                seen_names.add(name_lower)
                unique_entities.append(entity)
        
        return unique_entities
    
    def extract_entities_batch(self, reviews: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Extrai entidades de múltiplos comentários.
        
        Args:
            reviews: Lista de dicionários com 'content', 'app_name', 'date', 'version'
            
        Returns:
            Dicionário mapeando review_id para lista de entidades
        """
        results = {}
        
        for review in reviews:
            review_id = review.get('reviewId') or review.get('id', '')
            entities = self.extract_entities(
                review_content=review.get('content', ''),
                app_name=review.get('app_name', ''),
                review_date=review.get('date', ''),
                review_version=review.get('version', '')
            )
            results[review_id] = entities
        
        return results


def extract_entities_from_csv(csv_path: str, output_path: Optional[str] = None, 
                              limit: Optional[int] = None) -> Dict[str, List[Dict]]:
    """
    Extrai entidades de um CSV de avaliações.
    
    Args:
        csv_path: Caminho para CSV com avaliações
        output_path: Caminho para salvar resultados JSON (opcional)
        limit: Limite de avaliações para processar (opcional)
        
    Returns:
        Dicionário mapeando review_id para lista de entidades
    """
    import pandas as pd
    
    # Detectar separador
    with open(csv_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        separator = ';' if ';' in first_line else ','
    
    df = pd.read_csv(csv_path, sep=separator, encoding='utf-8')
    
    if limit:
        df = df.head(limit)
    
    extractor = EntityExtractor()
    
    reviews = []
    for _, row in df.iterrows():
        reviews.append({
            'reviewId': str(row.get('reviewId', '')),
            'content': str(row.get('content', '')),
            'app_name': str(row.get('app_name', '')),
            'date': str(row.get('date', '')),
            'version': str(row.get('version', ''))
        })
    
    results = extractor.extract_entities_batch(reviews)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extrai entidades de comentários de avaliações")
    parser.add_argument("--input", required=True, help="CSV com avaliações")
    parser.add_argument("--output", help="JSON de saída com entidades extraídas")
    parser.add_argument("--limit", type=int, help="Limite de avaliações para processar")
    
    args = parser.parse_args()
    
    results = extract_entities_from_csv(args.input, args.output, args.limit)
    print(f"Entidades extraídas de {len(results)} avaliações")
