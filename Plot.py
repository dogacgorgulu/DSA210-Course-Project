import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


le = LabelEncoder()


# Load the data
file_path = 'Hearthstone/data/ArenaData.xlsx'
data = pd.read_excel(file_path)

# Transform Class and Archetype to numeric values using LabelEncoder
label_encoders = {}
for column in ['Class', 'Archetype']:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# Save mappings for reference
for column, le in label_encoders.items():
    print(f"{column} mapping:")
    print(dict(zip(le.classes_, le.transform(le.classes_))))

# Create a scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='Reach', y='W')

# Add titles and labels
#plt.title('Scatter Plot of Wins vs Card Draw', fontsize=16)
#plt.xlabel('Card Draw', fontsize=12)
#plt.ylabel('Number of Wins (W)', fontsize=12)

corr = data.corr()  # Compute correlations
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Features')
plt.show()

archetype_avg_wins = data.groupby('Archetype')['W'].mean().sort_values()

# Bar plot of average wins by archetype
plt.figure(figsize=(10, 6))
sns.barplot(x=archetype_avg_wins.index, y=archetype_avg_wins.values, palette="viridis")
plt.xticks(rotation=45)
plt.title('Average Wins by Archetype')
plt.xlabel('Archetype')
plt.ylabel('Average Wins')
plt.show()

# Box plot for wins distribution by archetype
plt.figure(figsize=(12, 6))
sns.boxplot(x='Archetype', y='W', data=data, palette="Set2")
plt.xticks(rotation=45)
plt.title('Wins Distribution by Archetype')
plt.xlabel('Archetype')
plt.ylabel('Wins')
plt.show()

# Scatter plot of Tierscore vs Wins (if Tierscore is relevant)
plt.figure(figsize=(8, 5))
sns.scatterplot(x='Tierscore', y='W', hue='Archetype', data=data, palette="coolwarm")
plt.title('Tierscore vs Wins by Archetype')
plt.xlabel('Tierscore')
plt.ylabel('Wins')
plt.show()

# Display the plot
plt.grid(True)
plt.show()