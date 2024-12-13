import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import itertools

# Load the data
file_path = 'data/ArenaData.xlsx'
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

# Drop unnecessary features
features_to_drop = ['L', 'W-Coin', 'L-Coin', "Archetype", "Class",]  # Features to drop
data = data.drop(columns=features_to_drop)

data['Combine'] = data['First Turn Playable'] + data['3-Drops'] + data['Card Draw'] + data['Early Removals'] + data['4-Drops'] 

## Combinations of features
feature_search_space_pos = [
"First Turn Playable",
"3-Drops",
"Card Draw",
"Early Removals",
"4-Drops",
"Pings",
"Late-game",
"Large Removals",
"Board clear",
"5-Drops",
"Reach",
"Tierscore",
"2-Drops",]

pos_combs = []

for r in range(1, len(feature_search_space_pos) + 1):
    pos_combs.extend(itertools.combinations(feature_search_space_pos, r))

pos_combs = [list(comb) for comb in pos_combs]

results = []

for list in pos_combs:
    data['New'] = sum(data[key] for key in list)
    corr = data.corr()
    sorted_corr = corr['W'].sort_values(ascending=False)
    print(sorted_corr)

    results.append({
        'Combination': list,
        'Correlation': corr["W"]["New"]
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Find the best and worst combinations
best_combination = results_df.loc[results_df['Correlation'].idxmax()]
worst_combination = results_df.loc[results_df['Correlation'].idxmin()]

print(best_combination.to_string())
print(worst_combination.to_string())

# Compute correlations
# corr = data.corr()

# Print sorted correlations with 'W'
# sorted_corr = corr['W'].sort_values(ascending=False)
# print(sorted_corr)

# Heatmap of the full correlation matrix
# plt.figure(figsize=(12, 8))
# sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
# plt.title('Correlation Matrix of Features')
# plt.show()



