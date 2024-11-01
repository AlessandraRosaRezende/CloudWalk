import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import LabelEncoder

# Carregar dados
df = pd.read_csv('./data/transactional-sample.csv')

# Pré-processamento de dados para treinamento do modelo
df['card_number'] = LabelEncoder().fit_transform(df['card_number'])
X = df[['user_id', 'card_number', 'transaction_amount']]
y = df['has_cbk']

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Treinar o modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predizer e gerar matriz de confusão
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()
plt.title('Confusion Matrix for Fraud Detection Model')
plt.show()
plt.savefig('/data/confusion_matrix_plot.png')
