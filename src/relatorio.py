import pandas as pd

# Carregar os dados da planilha de transações
file_path = './data/transactional-sample.csv'
transactions = pd.read_csv(file_path)

# Convertendo a coluna de data para o formato datetime
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])

# Lista para armazenar DataFrames de transações suspeitas
suspicious_transactions = []

# Critério 1: Transações do mesmo usuário em diferentes dispositivos em horários próximos (menos de 1 hora de diferença)
suspicious_criterion_1 = transactions.sort_values(by=['user_id', 'transaction_date'])
suspicious_criterion_1['time_diff'] = suspicious_criterion_1.groupby('user_id')['transaction_date'].diff().dt.total_seconds() / 3600
suspicious_criterion_1 = suspicious_criterion_1[(suspicious_criterion_1['time_diff'] < 1) & (suspicious_criterion_1['time_diff'] > 0)]
suspicious_transactions.append(suspicious_criterion_1[['transaction_id']])

# Critério 2: Transações de alto valor para um usuário (acima de 2 vezes a média)
user_avg = transactions.groupby('user_id')['transaction_amount'].mean()
suspicious_criterion_2 = transactions[transactions.apply(lambda x: x['transaction_amount'] > 2 * user_avg.loc[x['user_id']], axis=1)]
suspicious_transactions.append(suspicious_criterion_2[['transaction_id']])

# Critério 3: Transações no mesmo dispositivo por diferentes usuários
device_usage = transactions.groupby('device_id')['user_id'].nunique()
shared_devices = device_usage[device_usage > 1].index
suspicious_criterion_3 = transactions[transactions['device_id'].isin(shared_devices)]
suspicious_transactions.append(suspicious_criterion_3[['transaction_id']])

# Critério 4: Usuários com múltiplos chargebacks
user_cbk_count = transactions[transactions['has_cbk'] == True].groupby('user_id').size()
multiple_cbk_users = user_cbk_count[user_cbk_count > 1].index
suspicious_criterion_4 = transactions[transactions['user_id'].isin(multiple_cbk_users) & (transactions['has_cbk'] == True)]
suspicious_transactions.append(suspicious_criterion_4[['transaction_id']])

# Critério 5: Usuários com múltiplos cartões
user_card_count = transactions.groupby('user_id')['card_number'].nunique()
multiple_card_users = user_card_count[user_card_count > 1].index
suspicious_criterion_5 = transactions[transactions['user_id'].isin(multiple_card_users)]
suspicious_transactions.append(suspicious_criterion_5[['transaction_id']])

# Critério 6: Cartões de múltiplos usuários
card_count = transactions.groupby('card_number')['user_id'].nunique()
multiple_card_count = card_count[card_count > 1].index
suspicious_criterion_6 = transactions[transactions['card_number'].isin(multiple_card_count)]
suspicious_transactions.append(suspicious_criterion_6[['transaction_id']])

# Compilar todas as transações suspeitas em um único DataFrame
suspicious_combined = pd.concat(suspicious_transactions).drop_duplicates().reset_index(drop=True)

# Compilar IDs de transações de cada critério em listas 
ids_crit1 = set(suspicious_criterion_1['transaction_id']) 
ids_crit2 = set(suspicious_criterion_2['transaction_id']) 
ids_crit3 = set(suspicious_criterion_3['transaction_id']) 
ids_crit4 = set(suspicious_criterion_4['transaction_id']) 
ids_crit5 = set(suspicious_criterion_5['transaction_id']) 
ids_crit6 = set(suspicious_criterion_6['transaction_id']) 

# Identificar transações presentes em pelo menos dois critérios (alerta)
alert_risk_ids = (ids_crit1 & ids_crit2) | (ids_crit1 & ids_crit3) | (ids_crit1 & ids_crit4) | (ids_crit1 & ids_crit5) | (ids_crit1 & ids_crit6) | \
(ids_crit2 & ids_crit3) | (ids_crit2 & ids_crit4) | (ids_crit2 & ids_crit5) | (ids_crit2 & ids_crit6) | \
(ids_crit3 & ids_crit4) | (ids_crit3 & ids_crit5) | (ids_crit3 & ids_crit6) | \
(ids_crit4 & ids_crit5) | (ids_crit4 & ids_crit6) | \
(ids_crit5 & ids_crit6)
alert_risk_transactions = transactions[transactions['transaction_id'].isin(alert_risk_ids)] 

# Salvar cada critério de transações suspeitas em arquivos CSV separados
suspicious_criterion_1.to_csv('./data/criterio_1_user_mesmo_dispsitivo.csv', index=False)
suspicious_criterion_2.to_csv('./data/criterio_2_alto_valor.csv', index=False)
suspicious_criterion_3.to_csv('./data/criterio_3_dispositivo_compartilhado.csv', index=False)
suspicious_criterion_4.to_csv('./data/criterio_4_chargebacks.csv', index=False)
suspicious_criterion_5.to_csv('./data/criterio_5_user_multiple_cards.csv', index=False)
suspicious_criterion_6.to_csv('./data/criterio_6_card_multiple_users.csv', index=False)

# Salvar transações de alto risco (coincidentes em múltiplos critérios) em um CSV separado
alert_risk_transactions.to_csv('./data/alerta.csv', index=False)

# Identificar transações presentes em pelo menos três critérios (alto risco) 
high_risk_ids = (ids_crit1 & ids_crit2 & ids_crit3) | (ids_crit1 & ids_crit2 & ids_crit4) | (ids_crit1 & ids_crit2 & ids_crit5) | (ids_crit1 & ids_crit2 & ids_crit6) | \
(ids_crit1 & ids_crit3 & ids_crit4) | (ids_crit1 & ids_crit3 & ids_crit5) | (ids_crit1 & ids_crit3 & ids_crit6) | \
(ids_crit1 & ids_crit4 & ids_crit5) | (ids_crit1 & ids_crit4 & ids_crit6) | (ids_crit1 & ids_crit5 & ids_crit6) | \
(ids_crit2 & ids_crit3 & ids_crit4) | (ids_crit2 & ids_crit3 & ids_crit5) | (ids_crit2 & ids_crit3 & ids_crit6) | \
(ids_crit2 & ids_crit4 & ids_crit5) | (ids_crit2 & ids_crit4 & ids_crit6) | (ids_crit3 & ids_crit4 & ids_crit5) | \
(ids_crit3 & ids_crit4 & ids_crit6) | (ids_crit3 & ids_crit5 & ids_crit6) | (ids_crit4 & ids_crit5 & ids_crit6) 
high_risk_transactions = transactions[transactions['transaction_id'].isin(high_risk_ids)] 

# Salvar transações de alto risco (coincidentes em múltiplos critérios) em um CSV separado
high_risk_transactions.to_csv('./data/alto_risco.csv', index=False)