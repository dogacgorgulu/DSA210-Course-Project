#
# Class mapping:
# {'Demon Hunter': 0, 'Druid': 1, 'Hunter': 2, 'Mage': 3, 'Paladin': 4, 'Priest': 5, 'Rogue': 6, 'Shaman': 7, 'Warlock': 8, 'Warrior': 9}
#
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Load the data
file_path = 'data/ArenaData_2.xlsx'
data = pd.read_excel(file_path)

# Create Win Rate column
data['Win Rate'] = data['W'] / (data['W'] + data['L'])

# Create Win Rates by Classes
class_win_rates = data.groupby('Class')['Win Rate'].mean()



# Bar Plot
class_win_rates.plot(kind='bar', figsize=(10, 6), title='Win Rate by Class')
plt.xlabel('Class')
plt.ylabel('Win Rate')
plt.show()

from scipy.stats import ttest_ind

# Filter Demon Hunter and other classes

# Classes win rates
demon_hunter_wr = data[data['Class'] == 'Demon Hunter']['Win Rate']
druid_wr = data[data['Class'] == 'Druid']['Win Rate']
hunter_wr = data[data['Class'] == 'Hunter']['Win Rate']
mage_wr = data[data['Class'] == 'Mage']['Win Rate']
paladin_wr = data[data['Class'] == 'Paladin']['Win Rate']
priest_wr = data[data['Class'] == 'Priest']['Win Rate']
rogue_wr = data[data['Class'] == 'Rogue']['Win Rate']
shaman_wr = data[data['Class'] == 'Shaman']['Win Rate']
warlock_wr = data[data['Class'] == 'Warlock']['Win Rate']
warrior_wr = data[data['Class'] == 'Warrior']['Win Rate']

other_classes_wr = data[data['Class'] != 'Demon Hunter']['Win Rate']

# T-test
t_stat, p_value = ttest_ind(demon_hunter_wr, other_classes_wr)
print("T-test results: t-statistic =", t_stat, ", p-value =", p_value)

# Calculate the total number of games played for each Class and Archetype
data['Total Games'] = data['W'] + data['L']
class_games = data.groupby('Class')['Total Games'].sum().sort_values()
archetype_games = data.groupby('Archetype')['Total Games'].sum().sort_values()

# Mean values
mean_class_games = class_games.mean()
mean_archetype_games = archetype_games.mean()

# Bar chart for games played by Class with mean line
plt.figure(figsize=(10, 6))
sns.barplot(x=class_games.index, y=class_games.values, palette="tab10")
plt.axhline(mean_class_games, color='red', linestyle='--', label=f'Mean: {mean_class_games:.1f}')
plt.title("Total Games Played by Class")
plt.xlabel("Class")
plt.ylabel("Total Games")
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Bar chart for games played by Archetype with mean line
plt.figure(figsize=(10, 6))
sns.barplot(x=archetype_games.index, y=archetype_games.values, palette="viridis")
plt.axhline(mean_archetype_games, color='red', linestyle='--', label=f'Mean: {mean_archetype_games:.1f}')
plt.title("Total Games Played by Archetype")
plt.xlabel("Archetype")
plt.ylabel("Total Games")
plt.xticks(rotation=45)
plt.legend()
plt.show()

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

# Basic Data Overview
print("\nDataset Head (After Encoding):")
print(data.head())

# Correlation Heatmap (with encoded columns)
plt.figure(figsize=(12, 8))
sns.heatmap(data.corr(method='pearson'), annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Correlation Heatmap (pearson)")
plt.show()

# Correlation Heatmap (with encoded columns)
plt.figure(figsize=(12, 8))
sns.heatmap(data.corr(method='spearman'), annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Correlation Heatmap (spearman)")
plt.show()

# Correlation Heatmap (with encoded columns)
plt.figure(figsize=(12, 8))
sns.heatmap(data.corr(method='kendall'), annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Correlation Heatmap (kendall)")
plt.show()

# Card Distribution by Class
card_columns = ["2-Drops", "3-Drops", "4-Drops", "5-Drops", "Late-game"]
card_distribution = data.groupby("Class")[card_columns].mean()

plt.figure(figsize=(10, 6))
sns.heatmap(card_distribution, annot=True, fmt=".1f", cmap="Blues", cbar=True)
plt.title("Average Card Distribution by Class")
plt.show()

# Wins vs. Tier Score by Class
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x="Tierscore", y="W", hue="Class", palette="tab10", s=100)
plt.title("Wins vs. Tier Score by Class")
plt.xlabel("Tier Score")
plt.ylabel("Wins")
plt.legend(title="Class")
plt.show()

# Save Correlation Data
correlation_matrix = data.corr()
correlation_matrix.to_csv("correlation_matrix_with_encoded_columns.csv")
print("Correlation matrix saved as 'correlation_matrix_with_encoded_columns.csv'.")

