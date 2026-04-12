"""
Script para organizar o projeto em pastas estruturadas
"""

import os
import shutil
from pathlib import Path

# Estrutura de organização
ESTRUTURA = {
    # Scripts principais
    'scripts': [
        'sentiment_analysis.py',
        'functional_correlation.py',
        'validate_model.py',
        'generate_backlog_report.py',
    ],
    
    # Scripts de análise
    'scripts/analysis': [
        'analyze_human_classification.py',
        'compare_human_vs_llm.py',
        'calculate_inter_annotator_agreement.py',
        'analyze_other_categories.py',
        'compare_models.py',
    ],
    
    # Scripts utilitários
    'scripts/utils': [
        'read_pptx.py',
        'get_real_stats.py',
        'show_negative_without_category.py',
        'generate_training_dataset.py',
    ],
    
    # Scripts relacionados a mixed sentiment
    'scripts/mixed': [
        'adicionar_sentimento_mixed.py',
        'identificar_mixed_exemplo.py',
        'atualizar_guia_mixed.py',
    ],
    
    # Scripts de criação de guias
    'scripts/guia': [
        'criar_guia_anotacao_completo_excel.py',
        'criar_guia_anotacao_excel.py',
    ],
    
    # Scripts de apresentação
    'scripts/presentation': [
        'update_presentation.py',
        'update_presentation_v2.py',
        'add_validation_section.py',
    ],
    
    # Datasets principais
    'data': [
        'app_review_dataset_carol.csv',
        'app_review_dataset_samuel.csv',
        'ground_truth_dataset.csv',
        'sentiment_results.csv',
        'functional_correlation_results.csv',
        'training_dataset.csv',
        'app_review_dataset_ex.csv',
        'app_review_dataset.csv',
        'app_review_apple_2025.csv',
        'sentiment_comparison_final.csv',
        'avaliacoes_negativas_sem_categoria.csv',
    ],
    
    # Documentação
    'docs': [
        'guia_anotacao_classificacao.md',
        'guia_anotacao_completo.xlsx',
        'guia_anotacao_exemplos.xlsx',
        'guia_anotacao_exemplos.csv',
        'metodologia_validacao_modelo.md',
        'resumo_validacao_completa.md',
    ],
    
    # Relatórios
    'reports': [
        'sentiment_report.md',
        'backlog_priorizado.md',
        'Backlog Priorizado - Aplicativo Bancário.md',
        'analise_classificacao_carol.md',
        'avaliacoes_negativas_sem_categoria.md',
        'comparacao_antes_depois.md',
        'ajustes_apresentacao_gestor.md',
        'report_daily_hoje.md',
        'report_daily_amanha.md',
        'Proximos_Passos_Daily.md',
        'inter_annotator_final.txt',
        'inter_annotator_results.txt',
    ],
}

# Arquivos para excluir (temporários ou duplicados)
ARQUIVOS_EXCLUIR = [
    '~$guia_anotacao_completo.xlsx',  # Arquivo temporário do Excel
    'ResultadosCorrelação Funcional.xlsx',  # Resultado antigo
]

def criar_pastas():
    """Cria a estrutura de pastas."""
    for pasta in ESTRUTURA.keys():
        Path(pasta).mkdir(parents=True, exist_ok=True)
        print(f"✓ Pasta criada/verificada: {pasta}")

def mover_arquivos():
    """Move arquivos para as pastas corretas."""
    movidos = 0
    nao_encontrados = []
    
    for pasta, arquivos in ESTRUTURA.items():
        for arquivo in arquivos:
            origem = Path(arquivo)
            destino = Path(pasta) / arquivo
            
            if origem.exists():
                # Criar pasta se não existir
                destino.parent.mkdir(parents=True, exist_ok=True)
                
                # Verificar se destino já existe (arquivo já movido)
                if destino.exists():
                    print(f"⚠️  Já existe: {pasta}/{arquivo} (pulando)")
                    movidos += 1
                else:
                    try:
                        # Mover arquivo
                        shutil.move(str(origem), str(destino))
                        print(f"✓ Movido: {arquivo} -> {pasta}/")
                        movidos += 1
                    except PermissionError:
                        print(f"⚠️  Arquivo em uso (pulando): {arquivo}")
                        nao_encontrados.append(arquivo)
            else:
                nao_encontrados.append(arquivo)
    
    print(f"\n✓ {movidos} arquivos movidos")
    if nao_encontrados:
        print(f"⚠️  {len(nao_encontrados)} arquivos não encontrados (podem já estar em outras pastas):")
        for arquivo in nao_encontrados[:10]:  # Mostrar apenas os primeiros 10
            print(f"   - {arquivo}")

def excluir_arquivos():
    """Exclui arquivos desnecessários."""
    excluidos = 0
    
    for arquivo in ARQUIVOS_EXCLUIR:
        caminho = Path(arquivo)
        if caminho.exists():
            try:
                caminho.unlink()
                print(f"✓ Excluído: {arquivo}")
                excluidos += 1
            except PermissionError:
                print(f"⚠️  Arquivo em uso (não foi possível excluir): {arquivo}")
    
    print(f"\n✓ {excluidos} arquivos excluídos")

def criar_readme():
    """Cria um README explicando a estrutura."""
    readme_content = """# Estrutura do Projeto

## Pastas Principais

### `scripts/`
Scripts principais de processamento:
- `sentiment_analysis.py` - Análise de sentimentos usando modelo BERTweet
- `functional_correlation.py` - Categorização funcional usando LLM (GPT-4o)
- `validate_model.py` - Validação do modelo contra ground truth humano
- `generate_backlog_report.py` - Geração de relatório de backlog priorizado

### `scripts/analysis/`
Scripts de análise e comparação:
- `analyze_human_classification.py` - Análise de classificações humanas
- `compare_human_vs_llm.py` - Comparação entre classificações humanas e LLM
- `calculate_inter_annotator_agreement.py` - Cálculo de acordo inter-anotadores (Kappa)

### `scripts/utils/`
Scripts utilitários:
- `read_pptx.py` - Leitura de apresentações PowerPoint
- `get_real_stats.py` - Extração de estatísticas reais dos datasets
- `generate_training_dataset.py` - Geração de datasets para treino

### `scripts/mixed/`
Scripts relacionados a sentimento misto:
- `adicionar_sentimento_mixed.py` - Adiciona coluna mixed aos datasets
- `identificar_mixed_exemplo.py` - Identifica exemplos de mixed

### `scripts/guia/`
Scripts de criação de guias de anotação:
- `criar_guia_anotacao_completo_excel.py` - Cria guia completo em Excel

### `scripts/presentation/`
Scripts de atualização de apresentações:
- `update_presentation_v2.py` - Atualiza apresentação PowerPoint

### `data/`
Datasets e dados:
- `app_review_dataset_carol.csv` - Classificações da Carol
- `app_review_dataset_samuel.csv` - Classificações do Samuel
- `ground_truth_dataset.csv` - Ground truth consolidado
- `sentiment_results.csv` - Resultados da análise de sentimentos
- `functional_correlation_results.csv` - Resultados da categorização funcional

### `docs/`
Documentação:
- `guia_anotacao_classificacao.md` - Guia completo de anotação (Markdown)
- `guia_anotacao_completo.xlsx` - Guia completo de anotação (Excel)

### `reports/`
Relatórios gerados:
- `sentiment_report.md` - Relatório de análise de sentimentos
- `backlog_priorizado.md` - Backlog priorizado

## Fluxo de Trabalho

1. **Análise de Sentimentos**: `scripts/sentiment_analysis.py`
   - Gera: `data/sentiment_results.csv`

2. **Categorização Funcional**: `scripts/functional_correlation.py`
   - Usa: `data/sentiment_results.csv`
   - Gera: `data/functional_correlation_results.csv`

3. **Validação**: `scripts/validate_model.py`
   - Compara resultados do LLM com ground truth humano
   - Gera métricas de precisão, recall, F1-score

4. **Geração de Backlog**: `scripts/generate_backlog_report.py`
   - Gera: `reports/backlog_priorizado.md`
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✓ README.md criado")

def main():
    print("="*60)
    print("ORGANIZANDO PROJETO")
    print("="*60)
    
    print("\n1. Criando estrutura de pastas...")
    criar_pastas()
    
    print("\n2. Movendo arquivos...")
    mover_arquivos()
    
    print("\n3. Excluindo arquivos desnecessários...")
    excluir_arquivos()
    
    print("\n4. Criando README...")
    criar_readme()
    
    print("\n" + "="*60)
    print("ORGANIZAÇÃO CONCLUÍDA")
    print("="*60)
    print("\nEstrutura criada:")
    print("  scripts/          - Scripts principais")
    print("  scripts/analysis/ - Scripts de análise")
    print("  scripts/utils/    - Scripts utilitários")
    print("  scripts/mixed/    - Scripts de mixed sentiment")
    print("  scripts/guia/     - Scripts de guias")
    print("  scripts/presentation/ - Scripts de apresentação")
    print("  data/             - Datasets")
    print("  docs/             - Documentação")
    print("  reports/          - Relatórios")

if __name__ == "__main__":
    main()

