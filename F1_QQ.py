import pandas as pd
import numpy as np
import pingouin as pg
import matplotlib.pyplot as plt

# Load data
df_c = pd.read_excel("data/ArenaData_categorical.xlsx")

# Calculate win rates
df_c['Win Rate'] = df_c['W'] / df_c['Total Matches']

# Display the first few rows to verify the data
print(df_c.head())

# Classes
classes = df_c['Class'].unique()

# Set fixed x and y limits
x_limit = (-2, 2)  # X-axis range
y_limit = (-2, 2)  # Y-axis range

# Define grid layout
cols = 4  # Number of columns
rows = int(np.ceil(len(classes) / cols))  # Calculate rows based on the number of classes

# Create a figure for the grid layout
fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5))  # Adjust figure size dynamically
axes = axes.flatten()  # Flatten axes for easier indexing

# Plot Q-Q plots
for i, cls in enumerate(classes):
    class_data = df_c[df_c['Class'] == cls]['Win Rate']
    
    # Perform Shapiro-Wilk test only if there are at least 3 observations
    if len(class_data) >= 3:
        shapiro_result = pg.normality(class_data)
        p_value = shapiro_result['pval'].values[0]
    else:
        p_value = None
    
    # Plot Q-Q plot on the current axis
    ax = axes[i]
    pg.qqplot(class_data, dist='norm', confidence=0.95, ax=ax)
    
    # Set fixed axis limits
    ax.set_xlim(x_limit)
    ax.set_ylim(y_limit)
    
    # Annotate the plot
    if p_value is not None:
        ax.set_title(f'{cls}\nShapiro-Wilk p = {p_value:.3f}', fontsize=10)
    else:
        ax.set_title(f'{cls}\n(Skipped Shapiro-Wilk Test)', fontsize=10)
    
    ax.set_xlabel('Theoretical Quantiles', fontsize=8)
    ax.set_ylabel('Sample Quantiles', fontsize=8)

# Hide unused subplots
for j in range(len(classes), len(axes)):
    fig.delaxes(axes[j])

# Adjust layout and add title
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Reserve space for the title
plt.suptitle('Q-Q Plots with 95% Confidence Interval by Class', fontsize=16, y=0.98)

# Save the figure as a single image
filename = "QQ_Plots_Grid.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')  # High-quality save
plt.show()