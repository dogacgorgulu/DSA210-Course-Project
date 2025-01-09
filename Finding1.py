import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
from scipy.stats import levene
import seaborn as sns
from pingouin import welch_anova
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from scipy.stats import anderson
from scipy.stats import chi2_contingency

##
## READ DATA
##

# df_c tonly includes categorical data
df_c = pd.read_excel("data/ArenaData_categorical.xlsx")

# df_q only includes quanitative data
df_q = pd.read_excel("data/ArenaData_quantitative.xlsx")

# Calculate winrates
df_c['Win Rate'] = df_c['W'] / df_c['Total Matches']
df_q['Win Rate'] = df_q['W'] / df_q['Total Matches']

print(df_c.head())
print(df_q.head())

## Null hypothesis: The mean win rate is equal across all classes. (FAILED TO REJECT)
## Alternative Hypothesis: There is a significant difference in the mean win rates among the classes.

# Group win rates by class
groups = [df_c[df_c['Class'] == cls]['Win Rate'] for cls in df_c['Class'].unique()]

# Perform ANOVA
f_stat, p_val = f_oneway(*groups)
print(f"ANOVA F-statistic: {f_stat}, p-value: {p_val}")

# F-statistic: 0.6326618402826653, p-value: 0.7780008552299287

##
## Validate ANOVA
##

## 1. Shapiro-Wilk Test for Normality

for cls in df_c['Class'].unique():
    size = len(df_c[df_c['Class'] == cls])
    print(f"Class: {cls}, Size: {size}")

# Normality Test for Class Summary
# for cls in df_c['Class'].unique():
#     stat, p = stats.shapiro(df_c[df_c['Class'] == cls]['Win Rate'])
#    print(f"{cls} Win Rates - Shapiro-Wilk Test Statistic: {stat}, p-value: {p}")

# Normality cannot assumed since Class: Druid, Size: 2 < 3.

# Perform Levene's Test
stat, p = levene(*groups)
print(f"Levene’s Test Statistic: {stat}, p-value: {p}")

# p-value: 0.6095329149643589 (Failed to reject)
# Data is HOMOGENEOUS

# Finding 1. The mean win rate is equal across all classes.

