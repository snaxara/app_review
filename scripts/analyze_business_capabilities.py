"""
Análise das BusinessCapabilities baseada em dados reais
"""

import json

# Carregar métricas dos comentários
with open('reports/metrics_caixa_100_comments.json', 'r', encoding='utf-8') as f:
    metrics = json.load(f)

print("=" * 80)
print("ANALISE DE BUSINESSCAPABILITIES - REFINAMENTO BASEADO EM DADOS REAIS")
print("=" * 80)

print("\n1. DISTRIBUICAO DE ISSUES POR BUSINESSCAPABILITY (COMENTARIOS)")
print("-" * 80)

capabilities = metrics.get('capability_statistics', {})
sorted_caps = sorted(capabilities.items(), key=lambda x: x[1].get('total_issues', 0), reverse=True)

for name, stats in sorted_caps:
    total_issues = stats.get('total_issues', 0)
    total_episodes = stats.get('total_episodes', 0)
    level = stats.get('level', 'N/A')
    capability_type = stats.get('capability_type', 'N/A')
    business_value = stats.get('business_value', 'N/A')
    
    print(f"\n{name}:")
    print(f"  Issues: {total_issues} | Episodios: {total_episodes}")
    print(f"  Nivel: {level} | Tipo: {capability_type} | Valor: {business_value}")

print("\n\n2. ANALISE DE COBERTURA")
print("-" * 80)

# Defeitos do app por área funcional (dados reais)
defect_distribution = {
    "Box Relacionamento Digital": 37,
    "Arrecadação e Convênios": 37,
    "Estruturantes de TI": 11,
    "Meios de Pagamento": 10,
    "Box Conta Digital": 2,
    "Pessoas": 1
}

print("\nDefeitos em producao por area funcional:")
for area, count in defect_distribution.items():
    print(f"  {area}: {count} defeitos")

print("\n\n3. MAPEAMENTO PROPOSTO: AREA FUNCIONAL -> BUSINESSCAPABILITY")
print("-" * 80)

mapping = {
    "Box Relacionamento Digital": [
        "Autenticação e Acesso",
        "Interface e Experiência do Usuário", 
        "Consulta de Saldo e Extrato"
    ],
    "Arrecadação e Convênios": [
        "Pagamentos e Boletos",
        "Transferências PIX"
    ],
    "Estruturantes de TI": [
        "Performance e Estabilidade",
        "Empréstimos e Crédito"
    ],
    "Meios de Pagamento": [
        "Pagamentos e Boletos"
    ],
    "Box Conta Digital": [
        "Gestão de Cadastro e Conta"
    ],
    "Pessoas": [
        "Interface e Experiência do Usuário"
    ]
}

for area, bcs in mapping.items():
    print(f"\n{area}:")
    for bc in bcs:
        if bc in capabilities:
            issues = capabilities[bc].get('total_issues', 0)
            print(f"  -> {bc} ({issues} issues nos comentarios)")

print("\n\n4. BUSINESSCAPABILITIES COM POUCAS ISSUES (< 5)")
print("-" * 80)

low_usage = [(name, stats) for name, stats in capabilities.items() 
             if stats.get('total_issues', 0) < 5]

for name, stats in sorted(low_usage, key=lambda x: x[1].get('total_issues', 0)):
    issues = stats.get('total_issues', 0)
    print(f"  {name}: {issues} issues")

print("\n\n5. RECOMENDACOES DE REFINAMENTO")
print("-" * 80)

print("""
Baseado na analise:

1. CAPABILITIES BEM COBERTAS (mantidas):
   - Performance e Estabilidade (33 issues)
   - Gestão de Cadastro e Conta (20 issues)
   - Atendimento ao Cliente (19 issues)
   - Empréstimos e Crédito (18 issues)
   - Pagamentos e Boletos (17 issues)
   - Interface e Experiência do Usuário (16 issues)
   - Autenticação e Acesso (15 issues)
   - Transferências PIX (12 issues)
   - Consulta de Saldo e Extrato (11 issues)

2. CAPABILITIES COM BAIXO USO (avaliar remocao ou ajuste):
   - Acesso Geográfico (2 issues) - pode ser mantida se houver necessidade futura
   - Serviços de Veículos (0 issues) - considerar remover se nao aplicavel ao app
   - Notificações e Alertas (poucas issues) - manter se relevante

3. CAPABILITIES VALIDADAS POR DADOS REAIS:
   - As capabilities principais correspondem bem aos defeitos em producao
   - Box Relacionamento Digital -> Autenticação, Interface, Consulta
   - Arrecadação e Convênios -> Pagamentos, PIX
   - Estruturantes de TI -> Performance, Empréstimos
""")
