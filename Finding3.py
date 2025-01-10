import pandas as pd
import matplotlib.pyplot as plt
import dcor
from scipy.stats import mannwhitneyu

# Null Hypothesis: The custom archetype does not significantly impacts win count.(REJECTED)
# Alternative Hypothesis: The custom archetype significantly impact win count.

# df_q only includes quanitative data
df_q = pd.read_excel("data/ArenaData_quantitative.xlsx")

# df_q['Win Rate'] = df_q['W'] / df_q['Total Matches']

# Drop unnecessary columns
columns_to_drop = ['L', 'Total Matches', 'Tierscore']
df = df_q.drop(columns=columns_to_drop)

print(df.head())

# Summary statistics
summary = df.describe()
print(summary)

# Compute Pearson correlation matrix
pearson_corr = df.corr(method='pearson')
pearson_corr_W = pearson_corr['W'].sort_values(ascending=False)
print(pearson_corr_W)

# Compute Spearman correlation matrix
spearman_corr = df.corr(method='spearman')
spearman_corr_W = spearman_corr['W'].sort_values(ascending=False)
print(spearman_corr_W)

# Calculate distance correlation with 'W'
dcor_values = {}
for column in df.columns:
    if column != "W":  # Skip correlation with itself
        dcor_values[column] = dcor.distance_correlation(df["W"], df[column])

# Convert to a sorted series
dcor_series = pd.Series(dcor_values).sort_values(ascending=False)
print(dcor_series)

# Plot the distance correlation values
plt.figure(figsize=(10, 6))
bars = plt.bar(dcor_series.index, dcor_series.values, color='skyblue', edgecolor='black')
plt.show()

# Identify the top correlated strategies
top_strategies = spearman_corr_W[spearman_corr_W.index != 'W'][:3].index  # Top 3 strategies
print(f"Top correlated strategies: {list(top_strategies)}")

# Calculate medians for thresholds
drops_median = df['5-Drops'].median()
early_removals_median = df['Early Removals'].median()
large_game_median = df['Late-game'].median()

# Define high strategy group
high_strategy_group = df[
    (df['5-Drops'] > drops_median - 2) & 
    (df['5-Drops'] <= drops_median + 2) & 
    (df['Early Removals'] > early_removals_median) & 
    ~((df['Late-game'] > large_game_median - 2) & (df['Late-game'] <= large_game_median + 2))
]['W']

# Define low strategy group (the rest)
low_strategy_group = df[
    ~(
        (df['5-Drops'] > drops_median - 2) & 
        (df['5-Drops'] <= drops_median + 2) & 
        (df['Early Removals'] > early_removals_median) & 
        ~((df['Late-game'] > large_game_median - 2) & (df['Late-game'] <= large_game_median + 2))
    )
]['W']

# Perform the Mann-Whitney U Test
u_stat, p_value = mannwhitneyu(high_strategy_group, low_strategy_group, alternative='two-sided')

# Output the test results
print(f"Mann-Whitney U Test Statistic: {u_stat}")
print(f"P-Value: {p_value}")

### U-Statistic: 348.5, P-Value: 0.0020171064658066206

if p_value < 0.05:
    print("Reject the null hypothesis: The strategy significantly impacts win count.")
else:
    print("Fail to reject the null hypothesis: No significant impact.")





