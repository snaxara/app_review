"""
Script principal para processar comentários e criar Knowledge Graph.

Este script integra a extração de entidades com o mapeamento para BusinessCapabilities,
criando um grafo completo no Neo4j que representa os problemas identificados nas
avaliações e suas relações com funcionalidades do aplicativo.
"""

import pandas as pd
import json
import uuid
import hashlib
from typing import Dict, List, Optional
from datetime import datetime
import sys
import os

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

from knowledge_graph.entity_extraction import EntityExtractor
from knowledge_graph.graph_manager import GraphManager
from knowledge_graph.create_capabilities import get_capability_by_category
from knowledge_graph.filter_generic_comments import filter_generic_comments

# Importar CATEGORIES do functional_correlation
try:
    from functional_correlation import CATEGORIES
except ImportError:
    # Fallback se não conseguir importar
    CATEGORIES = [
        "PIX", "Login/Autenticação", "Performance", "Interface/Usabilidade",
        "Empréstimos/Crédito", "Pagamentos/Boletos", "Saldo/Extrato",
        "Atendimento", "Cadastro/Conta", "Investimentos", "Segurança",
        "Notificações", "Questões geográficas",
        "Tarifas/Cobranças", "Outros"
    ]


def map_entity_to_capabilities(entity_name: str, entity_labels: List[str], 
                              categories: List[str], review_content: str = "") -> List[str]:
    """
    Mapeia uma entidade extraída para uma ou múltiplas BusinessCapability.
    Algumas entidades podem pertencer a múltiplas capabilities.
    
    Args:
        entity_name: Nome da entidade
        entity_labels: Labels da entidade (Issue, etc.)
        categories: Lista de categorias funcionais do comentário
        review_content: Conteúdo do comentário (para contexto adicional)
        
    Returns:
        Lista de categorias correspondentes (pode ter múltiplas)
    """
    entity_lower = entity_name.lower()
    capabilities = []
    
    # Entidades que podem ter múltiplas BusinessCapability
    multi_capability_entities = {
        'mudança de senha': ['Login/Autenticação', 'Segurança'],
        'alterar senha': ['Login/Autenticação', 'Segurança'],
        'trocar senha': ['Login/Autenticação', 'Segurança'],
        'senha': ['Login/Autenticação', 'Segurança'],  # Pode ser ambas
        'biometria': ['Login/Autenticação'],  # Principalmente autenticação
        'falta de confiança': ['Segurança'],
        'modo escuro': ['Interface/Usabilidade'],
        'dark mode': ['Interface/Usabilidade'],
        'tema escuro': ['Interface/Usabilidade'],
    }
    
    # Verificar primeiro se é uma entidade multi-capability
    for key, cap_list in multi_capability_entities.items():
        if key in entity_lower:
            capabilities.extend(cap_list)
            return list(set(capabilities))  # Remove duplicatas
    
    # Se não encontrou, usar mapeamento normal (retorna apenas uma)
    category = map_entity_to_capability(entity_name, entity_labels, categories, review_content)
    if category:
        return [category]
    return []


def map_entity_to_capability(entity_name: str, entity_labels: List[str], 
                            categories: List[str], review_content: str = "") -> Optional[str]:
    """
    Mapeia uma entidade extraída para uma BusinessCapability baseado nas categorias.
    
    Args:
        entity_name: Nome da entidade
        entity_labels: Labels da entidade (Issue, etc.)
        categories: Lista de categorias funcionais do comentário
        review_content: Conteúdo do comentário (para contexto adicional)
        
    Returns:
        Nome da categoria correspondente ou None
    """
    entity_lower = entity_name.lower()
    review_lower = review_content.lower() if review_content else ""
    
    # Mapeamento direto de nomes de entidades para categorias
    entity_to_category = {
        # PIX
        'pix': 'PIX',
        
        # Login/Autenticação (ordem: mais específico primeiro)
        'dificuldade para logar': 'Login/Autenticação',
        'dificuldade de logar': 'Login/Autenticação',
        'erro ao entrar na conta': 'Login/Autenticação',
        'erro ao entrar': 'Login/Autenticação',
        'erro para entrar': 'Login/Autenticação',
        'problemas para entrar': 'Login/Autenticação',
        'não reconhece biometria': 'Login/Autenticação',
        'biometria não funciona': 'Login/Autenticação',
        'reconhecimento biométrico': 'Login/Autenticação',
        'inserir senha': 'Login/Autenticação',
        'colocar senha': 'Login/Autenticação',
        'acesso ao aplicativo': 'Login/Autenticação',
        'falta de acesso para consulta': 'Login/Autenticação',
        'biometria': 'Login/Autenticação',
        'senha': 'Login/Autenticação',
        'login': 'Login/Autenticação',
        'autenticação': 'Login/Autenticação',
        'acesso': 'Login/Autenticação',
        'acesso a saldo': 'Login/Autenticação',  # Problema de acesso
        
        # Performance (ordem: mais específico primeiro)
        'app trava na hora de receber o pagamento': 'Performance',  # Travamento técnico, não problema de pagamento
        'problemas de abertura do app': 'Performance',
        'app não abre': 'Performance',
        'aplicativo não abre': 'Performance',
        'não abre o app': 'Performance',
        'não abre o aplicativo': 'Performance',
        'performance': 'Performance',
        'lentidão': 'Performance',
        'lento': 'Performance',
        'trava': 'Performance',
        'travamento': 'Performance',
        'travando': 'Performance',
        'fora do ar': 'Performance',
        'falha': 'Performance',
        'erro ao abrir': 'Performance',
        # 'não abre' será tratado abaixo com lógica especial
        'não funciona': 'Performance',
        'cai': 'Performance',
        'caindo': 'Performance',
        'estresse nos clientes': 'Performance',  # Consequência de problemas de performance
        'bugs': 'Performance',
        'falhas': 'Performance',
        'problemas técnicos': 'Performance',
        
        # Interface/Usabilidade (ordem: mais específico primeiro)
        'nova aparência da tela inicial': 'Interface/Usabilidade',
        'preferência pela tela inicial antiga': 'Interface/Usabilidade',
        'tela inicial': 'Interface/Usabilidade',
        'experiência do usuário': 'Interface/Usabilidade',
        'experiência do usuario': 'Interface/Usabilidade',
        'facilidade de uso': 'Interface/Usabilidade',
        'frustração do usuário': 'Interface/Usabilidade',
        'frustração do usuario': 'Interface/Usabilidade',
        'insatisfação do usuário': 'Interface/Usabilidade',
        'insatisfação do usuario': 'Interface/Usabilidade',
        'irritação do usuário': 'Interface/Usabilidade',
        'irritação do usuario': 'Interface/Usabilidade',
        'falta de opção no aplicativo': 'Interface/Usabilidade',
        'falta de opção': 'Interface/Usabilidade',
        'troca de data de fatura': 'Interface/Usabilidade',
        'troca de data': 'Interface/Usabilidade',
        'consulta de informações': 'Interface/Usabilidade',
        'consulta de informacoes': 'Interface/Usabilidade',
        'dificuldade com função débito': 'Interface/Usabilidade',
        'dificuldade com função debito': 'Interface/Usabilidade',
        'função débito': 'Interface/Usabilidade',
        'função debito': 'Interface/Usabilidade',
        'dificuldade em obter estorno': 'Interface/Usabilidade',
        'obter estorno': 'Interface/Usabilidade',
        'estorno': 'Interface/Usabilidade',
        'propaganda de produtos': 'Interface/Usabilidade',
        'propaganda': 'Interface/Usabilidade',
        'frustração dos usuários': 'Interface/Usabilidade',
        'desativar contatos de agenda para fazer pix': 'Interface/Usabilidade',
        'desativar contatos de agenda': 'Interface/Usabilidade',
        'desativar contatos': 'Interface/Usabilidade',
        'modo escuro': 'Interface/Usabilidade',
        'dark mode': 'Interface/Usabilidade',
        'tema escuro': 'Interface/Usabilidade',
        'interface': 'Interface/Usabilidade',
        'usabilidade': 'Interface/Usabilidade',
        'navegação': 'Interface/Usabilidade',
        'design': 'Interface/Usabilidade',
        
        # Empréstimos/Crédito (ordem: mais específico primeiro)
        'insatisfação com o limite do cartão': 'Empréstimos/Crédito',
        'limite não aumentado': 'Empréstimos/Crédito',
        'limite nao aumentado': 'Empréstimos/Crédito',
        'oferta de limite impossível de usar': 'Empréstimos/Crédito',
        'oferta de limite impossivel de usar': 'Empréstimos/Crédito',
        'pedido de novo cartão': 'Empréstimos/Crédito',
        'pedido de novo cartao': 'Empréstimos/Crédito',
        'problemas de obtenção de cartão': 'Empréstimos/Crédito',
        'problemas de obtencao de cartao': 'Empréstimos/Crédito',
        'obtenção de cartão': 'Empréstimos/Crédito',
        'obtencao de cartao': 'Empréstimos/Crédito',
        'limite do cartão': 'Empréstimos/Crédito',
        'limite do cartao': 'Empréstimos/Crédito',
        'limite': 'Empréstimos/Crédito',
        'atraso na entrega do cartão de crédito': 'Empréstimos/Crédito',
        'atraso na entrega do cartão': 'Empréstimos/Crédito',
        # Nota: 'cartão físico não chegou' mapeado para Outras Funcionalidades (decisão de negócio)
        'não consigo refinanciar': 'Empréstimos/Crédito',
        'refinanciar': 'Empréstimos/Crédito',
        'empréstimo': 'Empréstimos/Crédito',
        'crédito': 'Empréstimos/Crédito',
        'linha de crédito': 'Empréstimos/Crédito',
        'análise de crédito': 'Empréstimos/Crédito',
        
        # Pagamentos/Boletos
        'atraso na compensação de ipva': 'Pagamentos/Boletos',
        'atraso na compensação': 'Pagamentos/Boletos',
        'compensação de documento': 'Pagamentos/Boletos',
        'compensação': 'Pagamentos/Boletos',
        'ipva': 'Pagamentos/Boletos',
        'pagamento': 'Pagamentos/Boletos',
        'boleto': 'Pagamentos/Boletos',
        'erro ao fazer pagamento': 'Pagamentos/Boletos',
        
        # Saldo/Extrato
        'saldo incorreto': 'Saldo/Extrato',
        'não consigo acessar saldo': 'Saldo/Extrato',
        'saldo': 'Saldo/Extrato',
        'extrato': 'Saldo/Extrato',
        'problema de exibição de saldo': 'Saldo/Extrato',
        
        # Atendimento (ordem: mais específico primeiro)
        'falta de atenção ao cliente': 'Atendimento',
        'falta de atencao ao cliente': 'Atendimento',
        'telefone péssimo': 'Atendimento',
        'telefone ruim': 'Atendimento',
        'atendimento telefônico péssimo': 'Atendimento',
        'atendimento telefônico ruim': 'Atendimento',
        'atendimento automatizado insatisfatório': 'Atendimento',
        'atendimento automatizado': 'Atendimento',
        'enrolada no chat': 'Atendimento',
        'enrolado no chat': 'Atendimento',
        'problemas de comunicação': 'Atendimento',
        'mais de 15 minutos de espera sem atendimento': 'Atendimento',
        'espera sem atendimento': 'Atendimento',
        'atendimento': 'Atendimento',
        'atendimento ruim': 'Atendimento',
        'atendimento péssimo': 'Atendimento',
        'atendente': 'Atendimento',
        'menu de resposta automática': 'Atendimento',
        'dificuldade em falar com atendente': 'Atendimento',
        'problema na cabeça': 'Atendimento',  # Expressão idiomática sobre decisão ruim
        'falar com humano': 'Atendimento',
        'suporte': 'Atendimento',
        'suporte técnico': 'Atendimento',
        'chat de suporte': 'Atendimento',
        'chat': 'Atendimento',
        
        # Cadastro/Conta (ordem: mais específico primeiro)
        'não consegui atualizar meus dados': 'Cadastro/Conta',
        'problemas de abertura de conta': 'Cadastro/Conta',
        'não consigo abrir conta': 'Cadastro/Conta',
        'não dá pra abrir conta': 'Cadastro/Conta',
        'problemas para abrir conta': 'Cadastro/Conta',
        'abertura de conta': 'Cadastro/Conta',
        'cadastro': 'Cadastro/Conta',
        'conta': 'Cadastro/Conta',
        'acesso à conta': 'Cadastro/Conta',
        'atualização de dados': 'Cadastro/Conta',
        'atualizar dados': 'Cadastro/Conta',
        'atualizar cadastro': 'Cadastro/Conta',
        'falta de contato': 'Cadastro/Conta',  # Problema de comunicação relacionado a conta
        
        # Investimentos
        'propostas de contratos indesejados': 'Investimentos',
        'propostas de contratos': 'Investimentos',
        'problemas de resgate': 'Investimentos',
        'resgate': 'Investimentos',
        'não dá pra resgatar': 'Investimentos',
        'setor de investimento não atualizado': 'Investimentos',
        'setor de investimento': 'Investimentos',
        'fazer investimento': 'Investimentos',
        'investimento': 'Investimentos',
        'evolução patrimônio': 'Investimentos',
        'inconsistência de dados com b3': 'Investimentos',
        'inconsistência de dados': 'Investimentos',
        
        # Segurança (ordem: mais específico primeiro)
        'assinatura não autorizada de planos': 'Segurança',
        'assinatura nao autorizada de planos': 'Segurança',
        'assinatura não autorizada': 'Segurança',
        'assinatura nao autorizada': 'Segurança',
        'monitoramento': 'Segurança',
        'privacidade': 'Segurança',
        'falta de transparência': 'Segurança',
        'transparência': 'Segurança',  # Transparência relacionada a segurança/privacidade
        'espionagem': 'Segurança',
        'espionam': 'Segurança',
        'tentativas de intrusão': 'Segurança',
        'intrusão': 'Segurança',
        'falta de confiança': 'Segurança',
        'confiança': 'Segurança',
        'segurança': 'Segurança',
        'camadas de segurança': 'Segurança',
        'falta de camadas de segurança': 'Segurança',
        
        # Notificações
        'notificação': 'Notificações',
        'notificações': 'Notificações',
        
        # Tarifas/Cobranças
        'comparação com custo de arroz': 'Tarifas/Cobranças',
        'comparação com custo': 'Tarifas/Cobranças',
        'tarifa de 16': 'Tarifas/Cobranças',
        'desconto insuficiente': 'Tarifas/Cobranças',
        'desconto considerado insuficiente': 'Tarifas/Cobranças',
        'tarifa': 'Tarifas/Cobranças',
        'tarifas': 'Tarifas/Cobranças',
        'taxa': 'Tarifas/Cobranças',
        'taxas': 'Tarifas/Cobranças',
        'cobrança': 'Tarifas/Cobranças',
        'cobranças': 'Tarifas/Cobranças',
        'desconto': 'Tarifas/Cobranças',  # Quando mencionado em contexto de tarifa
        'juros': 'Tarifas/Cobranças',
        
        # Empréstimos/Crédito (adicionar mais específicos)
        'refinanciamento': 'Empréstimos/Crédito',
        'consignado': 'Empréstimos/Crédito',
        'cartão de crédito': 'Empréstimos/Crédito',
        'acompanhamento pelo app': 'Empréstimos/Crédito',  # Quando relacionado a cartão/empréstimo
        
        # Acesso Geográfico
        'ausência de agência': 'Questões geográficas',
        'não tem agência': 'Questões geográficas',
        'sem agência': 'Questões geográficas',
        'agência na cidade': 'Questões geográficas',
        'agência': 'Questões geográficas',
        
        # Outras Funcionalidades (genéricas ou não categorizáveis)
        'cartão físico não chegou': 'Outras Funcionalidades',  # Decisão de negócio: logística, não funcionalidade
        'falta de qualidade no serviço': 'Outras Funcionalidades',  # Genérico demais
        'péssimo': 'Outras Funcionalidades',  # Genérico demais
        'péssima': 'Outras Funcionalidades',  # Genérico demais
    }
    
    # Caso especial: "Problemas de Abertura" ou "não abre" - distinguir app vs conta
    # IMPORTANTE: Verificar contexto ANTES de usar mapeamento direto
    if 'abertura' in entity_lower or 'não abre' in entity_lower or 'app não abre' in entity_lower:
        # Verificar contexto do comentário para distinguir
        # PRIORIDADE 1: Se menciona explicitamente "abrir conta" ou "abertura de conta" → Cadastro
        if ('abrir conta' in review_lower or 'abertura de conta' in review_lower or 
            'abrir conta bancária' in review_lower or 'abrir primeiro a conta' in review_lower):
            return 'Cadastro/Conta'
        # PRIORIDADE 2: Se a entidade menciona "conta" → Cadastro
        elif 'conta' in entity_lower and ('abrir' in entity_lower or 'abertura' in entity_lower):
            return 'Cadastro/Conta'
        # PRIORIDADE 3: Se menciona "app não abre" ou "aplicativo não abre" → Performance
        elif ('app não abre' in entity_lower or 'aplicativo não abre' in entity_lower or
              'não abre' in entity_lower and 'conta' not in entity_lower):
            # Verificar contexto adicional: se menciona fazer pagamento, login, etc. → Performance
            if any(word in review_lower for word in ['fazer pagamento', 'entrar', 'logar', 'acessar', 'usar']):
                return 'Performance'
            # Se não menciona conta explicitamente, assumir problema de abertura do app
            return 'Performance'
    
    # Verificar mapeamento direto
    # Primeiro, buscar matches mais específicos (frases completas)
    # Ordenar por tamanho decrescente para pegar matches mais específicos primeiro
    sorted_items = sorted(entity_to_category.items(), key=lambda x: len(x[0]), reverse=True)
    
    for key, category in sorted_items:
        if key in entity_lower:
            return category
    
    # Se não encontrou mapeamento direto, usar primeira categoria do comentário
    if categories:
        return categories[0]
    
    return None


def process_review_to_graph(
    review: Dict,
    graph: GraphManager,
    extractor: EntityExtractor,
    category_to_capability_id: Dict[str, str],
    ingestion_run: Optional[str] = None,
) -> bool:
    """
    Processa um comentário e cria entidades e relacionamentos no grafo.
    
    Args:
        review: Dicionário com dados do comentário
        graph: Instância do GraphManager
        extractor: Instância do EntityExtractor
        category_to_capability_id: Mapeamento de categoria para ID de capacidade
        
    Returns:
        True se processado com sucesso
    """
    # Gerar ID único para o episódio
    # Se não tiver reviewId, criar baseado em hash do conteúdo + data para garantir unicidade
    review_id = review.get('reviewId')
    if not review_id or str(review_id).strip() == '':
        content = review.get('content', '')
        review_date = review.get('date', '')
        app_name = review.get('app_name', '')
        # Criar hash único baseado em conteúdo + data + app para garantir unicidade
        unique_string = f"{content}_{review_date}_{app_name}"
        review_id = hashlib.md5(unique_string.encode('utf-8')).hexdigest()
    
    review_id = str(review_id)
    content = review.get('content', '')
    app_name = review.get('app_name', '')
    review_date = review.get('date', '')
    review_version = review.get('version', '')
    
    # Obter categorias funcionais do comentário (se já processado)
    categories = []
    for cat in CATEGORIES:
        if review.get(cat, False) or review.get(cat.lower().replace('/', '_'), False):
            categories.append(cat)
    
    # Criar ou buscar entidade única do app
    app_entity_id = graph.get_or_create_app_entity(app_name)
    
    # Criar ou buscar entidade de versão
    version_entity_id = None
    if review_version and review_version != 'N/A':
        version_entity_id = graph.get_or_create_version_entity(review_version, app_name)
        if version_entity_id:
            graph.link_version_to_app(version_entity_id, app_entity_id)
    
    # Criar episódio (preservar conteúdo original)
    # Se já existir, não atualizar (preservar conteúdo original conforme metodologia)
    episode_created = graph.create_episode(
        episode_id=review_id,
        content=content,
        app_name=app_name,
        review_date=review_date,
        review_version=review_version,
        ingestion_run=ingestion_run,
    )
    
    # Se episódio já existia, não processar novamente (evitar duplicação de entidades)
    if not episode_created:
        print(f"  AVISO: Episódio {review_id} já existe, pulando processamento")
        return False
    
    # Linkar episódio com versão
    if version_entity_id:
        graph.link_episode_to_version(review_id, version_entity_id)
    
    # Extrair entidades do comentário (não inclui app nem versão)
    entities = extractor.extract_entities(
        review_content=content,
        app_name=app_name,
        review_date=review_date,
        review_version=review_version
    )
    
    # Filtrar entidades: remover app, versão e entidades genéricas
    filtered_entities = []
    generic_entities = ['aplicativo', 'app', 'aplicativo santander', 'santander', 'banco']
    
    # Entidades genéricas que não trazem informação útil (devem ser filtradas)
    generic_issue_patterns = [
        'péssimo', 'péssima', 'horrível', 'horrivel', 'ruim', 'lixo', 'terrível', 'terrivel',
        'falta de qualidade no serviço', 'falta de qualidade', 'qualidade do serviço',
        'serviço ruim', 'serviço péssimo', 'muito ruim', 'ruim demais'
    ]
    
    # Issues que NÃO devem ser criadas porque não são relacionadas ao app ou são muito genéricas
    # Essas Issues não podem ser mapeadas para nenhuma BusinessCapability do app
    invalid_issues = [
        # Issues muito genéricas sem contexto específico
        'erro', 'problema', 'dificuldade', 'confusão', 'decepção', 'expectativa',
        'mudança', 'identificação', 'dependência', 'correria',
        
        # Issues não relacionadas ao app (características do cliente ou serviços externos)
        'cliente de longa data', 'cliente de', 'cliente existente', 'cliente exi',
        'cartão não chegou', 'cartão não', 'cartão de',  # Entrega física não é funcionalidade do app
        'assinatura',  # Não relacionado ao app
        'avaliação',  # Não é uma issue
        'nome das',  # Não relacionado ao app
        'perda de',  # Muito genérico sem contexto
        'recompensa', 'sorteio',  # Não relacionado ao app
        'troca de',  # Não relacionado ao app
        'fatura fechada', 'fatura fec',  # Não relacionado ao app
        'serviço de', 'serviço ina',  # Muito genérico sem contexto específico
        
        # Issues que são características do cliente, não problemas do app
        'cliente', 'usuário', 'pessoa',
    ]
    
    # Issues genéricas que PODEM ser mantidas se tiverem contexto específico (serão mapeadas para "Outras Funcionalidades")
    # Exemplo: "Erro ao fazer PIX" é válido, mas "Erro" isolado não é
    generic_but_valid_patterns = [
        'erro ao', 'erro no', 'erro na', 'erro em',
        'problema com', 'problema no', 'problema na', 'problema de',
        'dificuldade para', 'dificuldade em', 'dificuldade no', 'dificuldade na',
    ]
    
    for entity in entities:
        entity_name_lower = entity.get('name', '').lower().strip()
        
        # Não incluir se for o nome do app, versão ou entidade genérica
        is_app_name = entity_name_lower == app_name.lower()
        is_version = entity_name_lower == review_version.lower()
        is_app_in_name = app_name.lower() in entity_name_lower
        is_generic = entity_name_lower in generic_entities
        
        # Verificar se é uma entidade genérica sem informação útil
        is_generic_issue = any(pattern in entity_name_lower for pattern in generic_issue_patterns)
        
        # Se for muito curta (menos de 3 caracteres) e genérica, filtrar
        is_too_generic = len(entity_name_lower) < 3 and entity_name_lower in ['ruim', 'péssimo', 'péssima']
        
        # Verificar se é uma Issue inválida (não relacionada ao app ou muito genérica)
        is_invalid_issue = any(invalid in entity_name_lower for invalid in invalid_issues)
        
        # Verificar se é uma Issue genérica mas válida (tem contexto específico)
        has_valid_context = any(pattern in entity_name_lower for pattern in generic_but_valid_patterns)
        
        # Se for Issue inválida E não tiver contexto válido, filtrar
        if is_invalid_issue and not has_valid_context:
            continue
        
        # Manter se não for genérica OU se for uma genérica que deve ser mantida
        if not (is_app_name or is_version or is_app_in_name or is_generic) and \
           (not is_generic_issue and not is_too_generic):
            filtered_entities.append(entity)
    
    # Criar entidades no grafo e linkar com capacidades
    for entity in filtered_entities:
        entity_name = entity.get('name', '')
        entity_labels = entity.get('labels', [])
        entity_summary = entity.get('summary', '')
        
        # Mapear entidade para BusinessCapability ANTES de criar (pode retornar múltiplas)
        capabilities = map_entity_to_capabilities(entity_name, entity_labels, categories, content)
        
        # Se não encontrou múltiplas, tentar mapeamento simples com contexto do comentário
        if not capabilities:
            category = map_entity_to_capability(entity_name, entity_labels, categories, content)
            
            # Verificação adicional para palavras-chave críticas
            if not category:
                entity_lower = entity_name.lower()
                
                # Autenticação
                auth_keywords = ['biometria', 'senha', 'login', 'autenticação', 'acesso']
                if any(keyword in entity_lower for keyword in auth_keywords):
                    category = 'Login/Autenticação'
                
                # Interface/Usabilidade
                if not category:
                    interface_keywords = ['experiência', 'experiencia', 'facilidade', 'frustração', 'frustracao', 
                                         'insatisfação', 'insatisfacao', 'irritação', 'irritacao', 'tela inicial',
                                         'aparência', 'aparencia', 'opção', 'opcao', 'consulta', 'estorno',
                                         'propaganda', 'débito', 'debito', 'troca de data']
                    if any(keyword in entity_lower for keyword in interface_keywords):
                        category = 'Interface/Usabilidade'
                
                # Empréstimos/Crédito
                if not category:
                    credito_keywords = ['limite', 'cartão', 'cartao', 'crédito', 'credito', 'empréstimo', 'emprestimo',
                                       'pedido de', 'obtenção', 'obtencao']
                    if any(keyword in entity_lower for keyword in credito_keywords):
                        category = 'Empréstimos/Crédito'
                
                # Atendimento
                if not category:
                    atendimento_keywords = ['atendimento', 'atendente', 'suporte', 'chat', 'telefone']
                    if any(keyword in entity_lower for keyword in atendimento_keywords):
                        category = 'Atendimento'
                
                # Segurança
                if not category:
                    seguranca_keywords = ['assinatura não autorizada', 'assinatura nao autorizada', 'segurança', 
                                         'seguranca', 'privacidade', 'monitoramento']
                    if any(keyword in entity_lower for keyword in seguranca_keywords):
                        category = 'Segurança'
            
            if category:
                capabilities = [category]
        
        # Se não conseguiu mapear para nenhuma BusinessCapability, não criar a entidade
        if not capabilities:
            continue
        
        # Buscar ou criar entidade por nome (agrupa entidades similares)
        entity_id = graph.get_or_create_entity_by_name(
            name=entity_name,
            labels=entity_labels,
            summary=entity_summary
        )
        
        # Linkar episódio com entidade
        graph.link_episode_to_entity(review_id, entity_id)
        
        # Se for Issue e temos versão, linkar issue -> versão (com contagem)
        if 'Issue' in entity_labels and version_entity_id:
            graph.link_issue_to_version(entity_id, version_entity_id)
        
        # Criar relacionamento(s) entidade -> BusinessCapability (pode ser múltiplos)
        for category in capabilities:
            if category in category_to_capability_id:
                capability_id = category_to_capability_id[category]
                
                # Criar relacionamento entidade -> BusinessCapability
                # t_valid = data do comentário (quando o fato ocorreu no mundo real)
                # t_created = agora (quando inserimos no sistema)
                fact = f"Entidade '{entity_name}' relacionada à capacidade '{category}' através do comentário"
                
                # Converter review_date para ISO format se necessário
                t_valid = review_date
                if review_date and not review_date.startswith('20'):
                    # Tentar parsear data se não estiver em formato ISO
                    try:
                        from datetime import datetime as dt
                        parsed_date = dt.strptime(review_date, '%Y-%m-%d')
                        t_valid = parsed_date.isoformat()
                    except:
                        t_valid = None
                
                graph.link_entity_to_capability(
                    entity_id=entity_id,
                    capability_id=capability_id,
                    fact=fact,
                    sentiment=review.get('sentiment_label', 'negative'),
                    t_valid=t_valid,
                    t_invalid=None  # Ainda válido
                )
    
    return True


def process_csv_to_graph(
    csv_path: str,
    graph: GraphManager,
    limit: Optional[int] = None,
    batch_size: int = 10,
    ingestion_run: Optional[str] = None,
) -> Dict:
    """
    Processa um CSV de avaliações e cria grafo completo.
    
    Args:
        csv_path: Caminho para CSV com avaliações
        graph: Instância do GraphManager
        limit: Limite de avaliações para processar
        batch_size: Tamanho do lote para processamento
        
    Returns:
        Estatísticas do processamento
    """
    # Detectar separador
    with open(csv_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        separator = ';' if ';' in first_line else ','
    
    df = pd.read_csv(csv_path, sep=separator, encoding='utf-8')
    
    # Filtrar comentários genéricos antes de processar (triagem)
    print("\nAplicando triagem para remover comentários genéricos...")
    df, filter_stats = filter_generic_comments(df, content_column='content')
    print(f"  Comentários genéricos filtrados: {filter_stats['filtered']} ({filter_stats['filter_percentage']:.1f}%)")
    print(f"  Comentários válidos para processar: {filter_stats['remaining']}")
    
    if limit:
        df = df.head(limit)
    
    # Carregar mapeamento categoria -> capability_id
    category_to_capability_id = {}
    for category in CATEGORIES:
        cap_id = get_capability_by_category(category, graph)
        if cap_id:
            category_to_capability_id[category] = cap_id
    
    if not category_to_capability_id:
        print("AVISO: Nenhuma BusinessCapability encontrada. Execute create_capabilities.py primeiro!")
        return {}
    
    extractor = EntityExtractor()
    
    stats = {
        'total_reviews': len(df),
        'processed': 0,
        'errors': 0,
        'entities_created': 0,
        'relationships_created': 0
    }
    
    tag = f" [ingestion_run={ingestion_run}]" if ingestion_run else ""
    print(f"Processando {len(df)} avaliações{tag}...")
    
    for idx, row in df.iterrows():
        try:
            # Garantir que temos um reviewId único
            review_id = str(row.get('reviewId', ''))
            if not review_id or review_id.strip() == '':
                # Se não tiver reviewId, criar baseado em hash do conteúdo + data
                content = str(row.get('content', ''))
                date = str(row.get('date', ''))
                app_name = str(row.get('app_name', ''))
                unique_string = f"{content}_{date}_{app_name}"
                review_id = hashlib.md5(unique_string.encode('utf-8')).hexdigest()
            
            review = {
                'reviewId': review_id,
                'content': str(row.get('content', '')),
                'app_name': str(row.get('app_name', '')),
                'date': str(row.get('date', '')),
                'version': str(row.get('version', '')),
                'sentiment_label': str(row.get('sentiment_label', 'negative'))
            }
            
            # Adicionar categorias se existirem no CSV
            for cat in CATEGORIES:
                col_name = cat.lower().replace('/', '_')
                if col_name in row:
                    review[cat] = bool(row[col_name])
            
            process_review_to_graph(
                review, graph, extractor, category_to_capability_id, ingestion_run=ingestion_run
            )
            stats['processed'] += 1
            
            if (idx + 1) % batch_size == 0:
                print(f"Processadas {idx + 1}/{len(df)} avaliações...")
        
        except Exception as e:
            print(f"Erro ao processar avaliação {idx}: {e}")
            stats['errors'] += 1
    
    print(f"\nProcessamento concluído!")
    print(f"  - Avaliações processadas: {stats['processed']}")
    print(f"  - Erros: {stats['errors']}")
    
    return stats


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Processa comentários e cria Knowledge Graph Temporal")
    parser.add_argument("--input", required=True, help="CSV com avaliações")
    parser.add_argument("--limit", type=int, help="Limite de avaliações para processar")
    parser.add_argument("--batch-size", type=int, default=10, help="Tamanho do lote")
    parser.add_argument(
        "--ingestion-run",
        default=None,
        metavar="TAG",
        help="Tag da rodada de carga no nó Episode (ex.: v2). Omitir = legado sem propriedade.",
    )
    
    args = parser.parse_args()
    
    with GraphManager() as graph:
        graph.initialize_indices()
        stats = process_csv_to_graph(
            args.input, graph, args.limit, args.batch_size, ingestion_run=args.ingestion_run
        )
        print(f"\nEstatísticas: {json.dumps(stats, indent=2)}")
