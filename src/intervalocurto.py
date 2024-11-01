import matplotlib.pyplot as plt
import pandas as pd

# Carregar dados
df = pd.read_csv('./data/transactional-sample.csv')

# Converter a coluna de tempo e calcular a diferença de tempo entre transações do mesmo usuário
df['datetime'] = pd.to_datetime(df['transaction_date'])
df = df.sort_values(by=['user_id', 'datetime'])
df['time_diff'] = df.groupby('user_id')['datetime'].diff().dt.seconds / 60  # diferença em minutos

# Filtrar transações com intervalos menores que 10 minutos
close_time_transactions = df[(df['time_diff'] <= 10) & (df['time_diff'] > 0)]

# Plotar transações de tempo próximo para um usuário específico
plt.figure(figsize=(12, 6))
user_data = close_time_transactions[close_time_transactions['user_id'] == close_time_transactions['user_id'].iloc[0]]
plt.plot(user_data['datetime'], user_data['transaction_amount'], marker='o')
plt.xlabel('Transaction Time')
plt.ylabel('Transaction Amount')
plt.title('Transactions in Close Time Intervals (User Example)')
plt.show()
plt.savefig('/data/close_time_interval_plot.png')
