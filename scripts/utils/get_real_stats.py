import pandas as pd

df = pd.read_csv('app_review_dataset_carol.csv', encoding='utf-8', sep=';')

total = len(df)
pos = df['positive'].sum()
neg = df['negative'].sum()
neu = df['neutral'].sum()

categories = ["PIX", "Login/Autenticação", "Performance", "Interface/Usabilidade", 
              "Empréstimos/Crédito", "Pagamentos/Boletos", "Saldo/Extrato", 
              "Atendimento", "Cadastro/Conta", "Investimentos", "Segurança", 
              "Notificações", "Questões geográficas", "Placas/Veículos", 
              "Tarifas/Cobranças", "Outros"]

print('='*60)
print('DADOS REAIS DO DATASET DA CAROL')
print('='*60)
print(f'\nTotal de avaliações: {total}')
print(f'Positivas: {pos} ({pos/total*100:.2f}%)')
print(f'Negativas: {neg} ({neg/total*100:.2f}%)')
print(f'Neutras: {neu} ({neu/total*100:.2f}%)')

print(f'\n--- Avaliações Negativas ---')
print(f'Total negativas: {neg}')
print(f'Negativas com categoria funcional: {(df[categories].sum(axis=1) > 0).sum()}')

print(f'\n--- Distribuição de Categorias (todas avaliações) ---')
for cat in categories:
    if cat in df.columns:
        count = df[cat].sum()
        if count > 0:
            print(f'{cat}: {int(count)}')

