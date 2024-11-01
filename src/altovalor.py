import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('./data/transactional-sample.csv')

# Calcular a média de transação para cada usuário e filtrar transações de alto valor
avg_user_amount = df.groupby('user_id')['transaction_amount'].mean()
df['high_value'] = df.apply(lambda x: x['transaction_amount'] > 2 * avg_user_amount[x['user_id']], axis=1)
high_value_transactions = df[df['high_value']]

# Plotar transações de alto valor
plt.figure(figsize=(10, 6))
plt.scatter(df['user_id'], df['transaction_amount'], color='blue', label='Regular Transactions')
plt.scatter(high_value_transactions['user_id'], high_value_transactions['transaction_amount'], color='red', label='High-Value Transactions')
plt.xlabel('User ID')
plt.ylabel('Transaction Amount')
plt.title('High-Value Transactions Detection')
plt.legend()
plt.show()
plt.savefig('/data/high_value_transactions_plot.png')
