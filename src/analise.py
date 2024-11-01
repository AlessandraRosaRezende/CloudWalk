import pandas as pd

# Carregar os dados da planilha de transações
file_path = './data/transactional-sample.csv'
transactions = pd.read_csv(file_path)

# 1. Critério 1: Transações do mesmo usuário em dispositivos diferentes em horários próximos
# Ordena as transações por usuário e data para calcular a diferença de tempo entre transações consecutivas
suspicious_criterion_1 = transactions.sort_values(by=['user_id', 'transaction_date'])

# Calcula a diferença de tempo em horas entre transações consecutivas do mesmo usuário
suspicious_criterion_1['time_diff'] = suspicious_criterion_1.groupby('user_id')['transaction_date'].diff().dt.total_seconds() / 3600

# Filtra transações onde o mesmo usuário usou dispositivos diferentes com menos de 1 hora de diferença
suspicious_criterion_1 = suspicious_criterion_1[(suspicious_criterion_1['time_diff'] < 1) & (suspicious_criterion_1['time_diff'] > 0)]

# 2. Critério 2: Transações de alto valor para um usuário (mais que o dobro da média)
# Calcula a média de transações para cada usuário
user_avg = transactions.groupby('user_id')['transaction_amount'].mean()

# Filtra transações acima de 2 vezes a média do valor de transação do usuário
suspicious_criterion_2 = transactions[transactions.apply(lambda x: x['transaction_amount'] > 2 * user_avg.loc[x['user_id']], axis=1)]

# 3. Critério 3: Transações no mesmo dispositivo por diferentes usuários
# Conta o número de usuários únicos por dispositivo
device_usage = transactions.groupby('device_id')['user_id'].nunique()

# Filtra dispositivos que foram utilizados por mais de um usuário
shared_devices = device_usage[device_usage > 1].index
suspicious_criterion_3 = transactions[transactions['device_id'].isin(shared_devices)]

# 4. Critério 4: Usuários com múltiplos chargebacks
# Conta o número de chargebacks por usuário
user_cbk_count = transactions[transactions['has_cbk'] == True].groupby('user_id').size()

# Identifica usuários com mais de um chargeback
multiple_cbk_users = user_cbk_count[user_cbk_count > 1].index

# Filtra as transações dos usuários com múltiplos chargebacks
suspicious_criterion_4 = transactions[transactions['user_id'].isin(multiple_cbk_users) & (transactions['has_cbk'] == True)]

# 5. Critério 5: Transações de um mesmo usuário com múltiplos cartões
# Conta o número de usuários únicos por cartão
card_number = transactions.groupby('card_number')['user_id'].nunique()

# Filtra dispositivos que foram utilizados por mais de um usuário
multiple_card = card_number[card_number > 1].index
suspicious_criterion_5 = transactions[transactions['card_number'].isin(multiple_card)]

# Combinação das Transações Suspeitas
# Compila todas as transações suspeitas em um único DataFrame e remove duplicatas
suspicious_combined = pd.concat([suspicious_criterion_1[['transaction_id']],
                                 suspicious_criterion_2[['transaction_id']],
                                 suspicious_criterion_3[['transaction_id']],
                                 suspicious_criterion_4[['transaction_id']],
                                 suspicious_criterion_5[['transaction_id']]]).drop_duplicates().reset_index(drop=True)




# Salvar como Excel
# Salvar o DataFrame em um arquivo Excel
suspicious_combined.to_excel('/mnt/data/transacoes_suspeitas.xlsx', index=False)

# Salvar como CSV
# Salvar o DataFrame em um arquivo CSV
suspicious_combined.to_csv('/mnt/data/transacoes_suspeitas.csv', index=False)

# Esses comandos gerarão arquivos chamados "transacoes_suspeitas.xlsx" e "transacoes_suspeitas.csv" na pasta indicada. É só rodar o código e os arquivos estarão prontos para download e uso na apresentação.


# Importa a biblioteca Pandas e cria um objeto ExcelWriter para salvar múltiplas abas
with pd.ExcelWriter('./data/transacoes_suspeitas_completas.xlsx') as writer:
    # Salva cada critério em uma aba diferente
    suspicious_criterion_1[['transaction_id']].to_excel(writer, sheet_name='Critério 1', index=False)
    suspicious_criterion_2[['transaction_id']].to_excel(writer, sheet_name='Critério 2', index=False)
    suspicious_criterion_3[['transaction_id']].to_excel(writer, sheet_name='Critério 3', index=False)
    suspicious_criterion_4[['transaction_id']].to_excel(writer, sheet_name='Critério 4', index=False)
    suspicious_criterion_5[['transaction_id']].to_excel(writer, sheet_name='Critério 5', index=False)
    
    # Salva todas as transações suspeitas combinadas em outra aba
    suspicious_combined.to_excel(writer, sheet_name='Todas Suspeitas', index=False)

# Esse código criará o arquivo "transacoes_suspeitas_completas.xlsx", com cada critério em uma aba própria e uma aba adicional chamada "Todas Suspeitas" para as transações combinadas.
