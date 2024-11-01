import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Carregar dados
df = pd.read_csv('./data/transactional-sample.csv')

# Contar quantos usuários usaram cada dispositivo
multiple_card = df.groupby('card_number')['user_id'].nunique()
multiple_card = multiple_card[multiple_card > 1]  # Filtrar mesmo usuário, múltiplos cartões

# Plotar o gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x=multiple_card.index, y=multiple_card.values, palette="viridis")
plt.xlabel('Card Number')
plt.ylabel('Number of Unique Users')
plt.title('One user multiple cards')
plt.xticks(rotation=45)
plt.show()
plt.savefig('/data/,ultiple_cards_plot.png')