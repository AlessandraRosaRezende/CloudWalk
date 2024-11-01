import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from fpdf import FPDF

# Generate sample plots to include in PDF

# Sample data for visualizations
np.random.seed(42)
user_ids = np.random.randint(1, 20, 100)
amounts = np.random.normal(500, 150, 100)
time_diffs = np.abs(np.random.normal(15, 5, 100))

# 1. High-Value Transactions Scatter Plot
plt.figure(figsize=(6, 4))
plt.scatter(user_ids, amounts, color='blue', label='Regular Transactions')
plt.scatter(user_ids, amounts + 300, color='red', label='High-Value Transactions')
plt.xlabel('User ID')
plt.ylabel('Transaction Amount')
plt.title('High-Value Transactions Detection')
plt.legend()
plt.savefig('./data/high_value_transactions_plot.png')
plt.close()

# 2. Close Time Interval Transactions Line Plot
plt.figure(figsize=(6, 4))
plt.plot(np.sort(time_diffs)[:10], amounts[:10], marker='o')
plt.xlabel('Transaction Time Difference (min)')
plt.ylabel('Transaction Amount')
plt.title('Close Time Interval Transactions')
plt.savefig('./data/close_time_interval_plot.png')
plt.close()

# 3. Shared Device Usage Bar Plot
device_ids = np.random.choice(['device_1', 'device_2', 'device_3', 'device_4'], 100)
unique_users_per_device = pd.Series(device_ids).value_counts()
plt.figure(figsize=(6, 4))
sns.barplot(x=unique_users_per_device.index, y=unique_users_per_device.values, palette="viridis")
plt.xlabel('Device ID')
plt.ylabel('Number of Unique Users')
plt.title('Devices Shared by Multiple Users')
plt.savefig('./data/shared_device_usage_plot.png')
plt.close()

# 4. Multiple cards Bar Plot
cards_number = np.random.choice(['card_1', 'card_2', 'card_3', 'card_4'], 100)
unique_users_per_cards = pd.Series(cards_number).value_counts()
plt.figure(figsize=(6, 4))
sns.barplot(x=unique_users_per_cards.index, y=unique_users_per_cards.values, palette="viridis")
plt.xlabel('Card number')
plt.ylabel('Number of Unique Users')
plt.title('Multiple Cards by Users')
plt.savefig('./data/multiple_cards_plot.png')
plt.close()

# 5. One Card Multiple users Bar Plot
cards_count = np.random.choice(['card_1', 'card_2', 'card_3', 'card_4'], 100)
users_multiple_card = pd.Series(cards_count).value_counts()
plt.figure(figsize=(6, 4))
sns.barplot(x=users_multiple_card.index, y=users_multiple_card.values, palette="viridis")
plt.xlabel('Unique Card number')
plt.ylabel('Users number')
plt.title('One card multiple users')
plt.savefig('./data/one_card_mult_usersplot.png')
plt.close()

# 5. Confusion Matrix for Machine Learning Model
# Encode data for machine learning
# df = pd.DataFrame({'user_id': user_ids, 'device_id': device_ids, 'transaction_amount': amounts, 'has_cbk': np.random.randint(0, 2, 100)})
# df['device_id'] = LabelEncoder().fit_transform(df['device_id'])
# X = df[['user_id', 'device_id', 'transaction_amount']]
# y = df['has_cbk']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# model = RandomForestClassifier(n_estimators=10, random_state=42)
# model.fit(X_train, y_train)
# y_pred = model.predict(X_test)
# cm = confusion_matrix(y_test, y_pred)

# # Save confusion matrix plot
# plt.figure(figsize=(6, 4))
# sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=['Non-Fraud', 'Fraud'], yticklabels=['Non-Fraud', 'Fraud'])
# plt.xlabel("Predicted")
# plt.ylabel("Actual")
# plt.title("Confusion Matrix for Fraud Detection Model")
# plt.savefig('./data/confusion_matrix_plot.png')
# plt.close()

# Create detailed PDF with visuals and explanations
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title Slide
pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Fraud Detection Case Analysis Presentation", ln=True, align="C")

# Slide 1: High-Value Transactions
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, "1. High-Value Transactions Analysis", ln=True)
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, """
    Code Explanation:
    - We use a scatter plot to display transaction values across users.
    - Red dots indicate high-value transactions exceeding twice the user's average.
    - Purpose: Highlight unusually large transactions that may indicate suspicious activity.

    Visualization:""")
pdf.image('./data/high_value_transactions_plot.png', x=30, w=150)

# Slide 2: Close Time Interval Transactions
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, "2. Close Time Interval Transactions Analysis", ln=True)
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, """
    Code Explanation:
    - This line plot shows transaction amounts over time differences within close intervals.
    - Quick successive transactions can indicate abnormal behavior.

    Visualization:""")
pdf.image('./data/close_time_interval_plot.png', x=30, w=150)

# Slide 3: Shared Device Usage
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, "3. Shared Device Usage Analysis", ln=True)
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, """
    Code Explanation:
    - This bar chart displays the number of unique users accessing each device.
    - Shared devices suggest potential fraud hotspots, like public terminals or compromised devices.

    Visualization:""")
pdf.image('./data/shared_device_usage_plot.png', x=30, w=150)

# Slide 4: Multiple cards
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, "4. Multiple Cards Analysis", ln=True)
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, """
    Code Explanation:
    - This bar chart displays the number of unique users using multiple cards.
    - Multiple cards suggest potential fraud hotspots.

    Visualization:""")
pdf.image('./data/multiple_cards_plot.png', x=30, w=150)

# # Slide 5: Machine Learning Model - Confusion Matrix
# pdf.set_font("Arial", "B", 14)
# pdf.cell(200, 10, "4. Machine Learning Model Evaluation", ln=True)
# pdf.set_font("Arial", "", 12)
# pdf.multi_cell(0, 10, """
#     Code Explanation:
#     - The confusion matrix visualizes the model's ability to distinguish fraud from legitimate transactions.
#     - True Positives (TP): Correctly identified frauds.
#     - False Positives (FP): Legitimate transactions flagged as fraud.
#     - True Negatives (TN): Legitimate transactions correctly identified.
#     - False Negatives (FN): Fraudulent transactions missed.

#     Visualization:""")
# pdf.image('./data/confusion_matrix_plot.png', x=30, w=150)

# Save the updated PDF
pdf_output_path_updated = "./data/Updated_Fraud_Detection_Case_Analysis_Presentation.pdf"
pdf.output(pdf_output_path_updated)

pdf_output_path_updated
