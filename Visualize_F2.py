import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pingouin as pg

# Load data
df_c = pd.read_excel("data/ArenaData_categorical.xlsx")

# Calculate win rates
df_c['Win Rate'] = df_c['W'] / df_c['Total Matches']

# Display the first few rows to verify the data
print(df_c.head())

# Group data by class for win rates
classes = df_c['Archetype'].unique()
groups = [df_c[df_c['Archetype'] == cls]['Win Rate'] for cls in classes]

# Boxplot for win rate distribution by Archetype
plt.figure(figsize=(10, 6))
sns.boxplot(x='Archetype', y='Win Rate', data=df_c, meanline=True, showmeans=True, meanprops={"color": "red"})
plt.title('Win Rate Distribution by Archetype', fontsize=16)
plt.xlabel('Archetype', fontsize=14)
plt.ylabel('Win Rate', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Scatter plot with mean lines for win rate per draft
plt.figure(figsize=(12, 8))

for i, group_data in enumerate(groups):
    # Scatter points for each Archetype
    x_coords = np.full_like(group_data, i + 1, dtype=float)  # x-coordinates for the group
    plt.scatter(x_coords, group_data, label=classes[i], s=50, alpha=0.7)

    # Mean line for each Archetype
    mean = group_data.mean()
    plt.hlines(mean, i + 0.8, i + 1.2, colors='red', linestyles='--', linewidth=2, label=None)

# Customize plot
plt.xticks(range(1, len(classes) + 1), classes, fontsize=12)
plt.xlabel('Archetype', fontsize=14)
plt.ylabel('Win Rate', fontsize=14)
plt.title('Win Rate by Class (With Means) per Draft', fontsize=16)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# Add legend
plt.legend(title="Archetype", fontsize=10, loc='upper right', bbox_to_anchor=(1.2, 1.0))
plt.show()

# Classes
classes = df_c['Archetype'].unique()

# Define the grid layout dynamically
num_classes = len(classes)
cols = 3  # Number of columns
rows = int(np.ceil(num_classes / cols))  # Calculate rows based on the number of classes

# Set figure size dynamically based on the number of rows
plt.figure(figsize=(cols * 5, rows * 5))  # Scale width and height proportionally

for i, cls in enumerate(classes, 1):
    class_data = df_c[df_c['Archetype'] == cls]['Win Rate']
    
    # Initialize variables
    shapiro_result = None
    p_value = None
    
    # Perform Shapiro-Wilk test only if there are at least 3 observations
    if len(class_data) >= 3:
        shapiro_result = pg.normality(class_data)
        p_value = shapiro_result['pval'].values[0]
    
    # Plot Q-Q plot
    ax = plt.subplot(rows, 3, i)
    pg.qqplot(class_data, dist='norm', confidence=0.95, ax=ax)
    
    # Annotate the plot
    if p_value is not None:
        ax.set_title(f'{cls}\nShapiro-Wilk p = {p_value:.3f}', fontsize=10)
    else:
        ax.set_title(f'{cls}\n(Skipped Shapiro-Wilk Test)', fontsize=10)
    
    ax.set_xlabel('Theoretical Quantiles', fontsize=8)
    ax.set_ylabel('Sample Quantiles', fontsize=8)

# Adjust layout and add title
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.suptitle('Q-Q Plots with 95% Confidence Interval by Archetype', fontsize=16, y=0.98)
plt.show()