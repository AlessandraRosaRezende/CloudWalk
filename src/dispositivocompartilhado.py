import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Carregar dados
df = pd.read_csv('./data/transactional-sample.csv')

# Contar quantos usuários usaram cada dispositivo
shared_device = df.groupby('device_id')['user_id'].nunique()
shared_device = shared_device[shared_device > 1]  # Filtrar dispositivos compartilhados

# Plotar o gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x=shared_device.index, y=shared_device.values, palette="viridis")
plt.xlabel('Device ID')
plt.ylabel('Number of Unique Users')
plt.title('Devices Shared by Multiple Users')
plt.xticks(rotation=45)
plt.show()
plt.savefig('/data/shared_device_usage_plot.png')
