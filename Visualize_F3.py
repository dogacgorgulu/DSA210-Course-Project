import pandas as pd
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import dcor


def plot_quadratic_with_x_median(x_data, y_data):
    """
    Fits a quadratic model to the data, plots the data and the fitted curve,
    and highlights the median and ±3 region for the x-axis.

    Parameters:
        x_data (array-like): Independent variable values.
        y_data (array-like): Dependent variable values.

    Returns:
        None
    """
    # Define a quadratic function
    def quadratic(x, a, b, c):
        return a * x**2 + b * x + c

    # Fit the quadratic model
    params, _ = curve_fit(quadratic, x_data, y_data)

    # Generate fitted curve
    x_range = np.linspace(min(x_data), max(x_data), 500)
    y_fit = quadratic(x_range, *params)

    # Calculate median and ±3 region for x_data
    x_median = np.median(x_data)
    x_upper = x_median + 2
    x_lower = x_median - 2

    # Plot data and fitted curve
    plt.figure(figsize=(10, 6))
    plt.scatter(x_data, y_data, label='Data', alpha=0.7, color='blue')
    plt.plot(x_range, y_fit, color='red', label='Quadratic Fit')

    # Add median and ±3 range for x-axis
    plt.axvline(x=x_median, color='green', linestyle='--', linewidth=1.5, label=f'Median (x): {x_median:.2f}')
    plt.axvline(x=x_upper, color='orange', linestyle='--', linewidth=1.5, label=f'Median +3: {x_upper:.2f}')
    plt.axvline(x=x_lower, color='orange', linestyle='--', linewidth=1.5, label=f'Median -3: {x_lower:.2f}')
    plt.fill_betweenx([min(y_data), max(y_data)], x_lower, x_upper, color='orange', alpha=0.2, label='Median ±3 Region (x)')

    # Customize the plot
    plt.xlabel('5-Drops', fontsize=12)
    plt.ylabel('Win Count', fontsize=12)
    plt.title('Non-Linear Regression Curve with Median and ±3 Region', fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # Show the plot
    plt.tight_layout()
    plt.show()

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

x_data = df['Late-game']
y_data = df['W']
plot_quadratic_with_x_median(x_data, y_data)

x_data = df['Early Removals']
y_data = df['W']
plot_quadratic_with_x_median(x_data, y_data)

x_data = df['5-Drops']
y_data = df['W']
plot_quadratic_with_x_median(x_data, y_data)

# Compute Pearson correlation matrix
pearson_corr = df.corr(method='pearson')
pearson_corr_W = pearson_corr['W'].sort_values(ascending=False)
pearson_corr_W = pearson_corr_W.drop('W')
print(pearson_corr_W)

# Compute Spearman correlation matrix
spearman_corr = df.corr(method='spearman')
spearman_corr_W = spearman_corr['W'].sort_values(ascending=False)
spearman_corr_W = spearman_corr_W.drop('W')
print(spearman_corr_W)

## Bar chart (Pearson)
# Create the bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(pearson_corr_W.index, pearson_corr_W.values, edgecolor='black')

# Add threshold lines
plt.axhline(y=0.2, color='red', linestyle='--', linewidth=1.5, label='Threshold: 0.2')
plt.axhline(y=-0.2, color='red', linestyle='--', linewidth=1.5, label='Threshold: -0.2')

# Add text annotations on the threshold lines
plt.text(len(pearson_corr_W) - 2, 0.22, 'Low correlation', color='red', fontsize=10)
plt.text(len(pearson_corr_W) - 2, -0.28, 'Low correlation', color='red', fontsize=10)

# Customize the chart
plt.title('Pearson Correlation (Win Count)', fontsize=14)
plt.xlabel('Attributes', fontsize=12)
plt.ylabel('Correlation', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.ylim(-1, 1)  # Ensure full correlation range is visible
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Add values on top of the bars
for bar in bars:
    height = bar.get_height()
    # Adjust position: above for positive bars, below for negative bars
    offset = 0.02 if height >= 0 else -0.02
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # x-coordinate
        height + offset,  # y-coordinate with offset
        f'{height:.2f}',  # Format value to 2 decimal places
        ha='center', va='bottom' if height >= 0 else 'top',  # Adjust alignment
        fontsize=10, color='black'
    )
# Show the plot
plt.tight_layout()
plt.show()

## Bar chart (Spearman)
# Create the bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(spearman_corr_W.index, spearman_corr_W.values, edgecolor='black')

# Add threshold lines
plt.axhline(y=0.2, color='red', linestyle='--', linewidth=1.5, label='Threshold: 0.2')
plt.axhline(y=-0.2, color='red', linestyle='--', linewidth=1.5, label='Threshold: -0.2')

# Add text annotations on the threshold lines
plt.text(len(spearman_corr_W) - 2, 0.22, 'Low correlation', color='red', fontsize=10)
plt.text(len(spearman_corr_W) - 2, -0.28, 'Low correlation', color='red', fontsize=10)

# Customize the chart
plt.title('Spearman Correlation (Win Count)', fontsize=14)
plt.xlabel('Attributes', fontsize=12)
plt.ylabel('Correlation', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.ylim(-1, 1)  # Ensure full correlation range is visible
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Add values on top of the bars
for bar in bars:
    height = bar.get_height()
    # Adjust position: above for positive bars, below for negative bars
    offset = 0.02 if height >= 0 else -0.02
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # x-coordinate
        height + offset,  # y-coordinate with offset
        f'{height:.2f}',  # Format value to 2 decimal places
        ha='center', va='bottom' if height >= 0 else 'top',  # Adjust alignment
        fontsize=10, color='black'
    )
# Show the plot
plt.tight_layout()
plt.show()

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
bars = plt.bar(dcor_series.index, dcor_series.values, edgecolor='black')

# Annotate the values on top of the bars
for bar in bars:
    height = bar.get_height()
    offset = 0.02 if height >= 0 else -0.02
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + offset,
        f'{height:.2f}',
        ha='center', va='bottom' if height >= 0 else 'top',
        fontsize=10, color='black'
    )

# Add a threshold line (optional)
plt.axhline(y=0.2, color='red', linestyle='--', linewidth=1.5, label='Threshold: 0.2')
plt.axhline(y=-0.2, color='red', linestyle='--', linewidth=1.5)

plt.text(len(spearman_corr_W) - 2, 0.22, 'Low correlation', color='red', fontsize=10)

# Add labels and grid
plt.title('Distance Correlation (Win Count)', fontsize=14)
plt.xlabel('Attributes', fontsize=12)
plt.ylabel('Distance Correlation', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.ylim(0, 1)  # Distance correlation is always between 0 and 1
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()



# Calculate medians for thresholds
drops_median = df['5-Drops'].median()
early_removals_median = df['Early Removals'].median()
large_game_median = df['Late-game'].median()

# Combine high and low strategy groups into a new DataFrame for visualization
high_strategy_group = df[
    (df['5-Drops'] > drops_median - 2) & 
    (df['5-Drops'] <= drops_median + 2) & 
    (df['Early Removals'] > early_removals_median) & 
    ~((df['Late-game'] > large_game_median - 2) & (df['Late-game'] <= large_game_median + 2))
]['W']

low_strategy_group = df[
    ~(
        (df['5-Drops'] > drops_median - 2) & 
        (df['5-Drops'] <= drops_median + 2) & 
        (df['Early Removals'] > early_removals_median) & 
        ~((df['Late-game'] > large_game_median - 2) & (df['Late-game'] <= large_game_median + 2))
    )
]['W']

# Create a DataFrame for visualization
visualization_df = pd.DataFrame({
    'Group': ['Custom Archetype'] * len(high_strategy_group) + ['Others'] * len(low_strategy_group),
    'W': pd.concat([high_strategy_group, low_strategy_group])
})

# Create a boxplot
plt.figure(figsize=(8, 6))
visualization_df.boxplot(by='Group', column='W', grid=False)
plt.title('Comparison of Win Counts between Custom Archetype and the rest')
plt.suptitle('')  # Removes the default title
plt.xlabel('Archetypes')
plt.ylabel('Wins')
plt.show()
