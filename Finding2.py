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

## Null hypothesis: The mean win rate is equal across all Archetypes. (FAILED TO REJECT)
## Alternative Hypothesis: There is a significant difference in the mean win rates among the archetypes.

# Group win rates by archetype
groups = [df_c[df_c['Archetype'] == cls]['Win Rate'] for cls in df_c['Archetype'].unique()]

# Perform ANOVA
f_stat, p_val = f_oneway(*groups)
print(f"ANOVA F-statistic: {f_stat}, p-value: {p_val}")

# ANOVA F-statistic: 1.044284028884457, p-value: 0.3936552667822725
# fail to reject

##
## Validate ANOVA
##

## 1. Shapiro-Wilk Test for Normality

for cls in df_c['Archetype'].unique():
    size = len(df_c[df_c['Archetype'] == cls])
    print(f"Archetype: {cls}, Size: {size}")

# Normality Test for Archetype Summary
for cls in df_c['Archetype'].unique():
    stat, p = stats.shapiro(df_c[df_c['Archetype'] == cls]['Win Rate'])
    print(f"{cls} Win Rates - Shapiro-Wilk Test Statistic: {stat}, p-value: {p}")

# Tempo Win Rates - Shapiro-Wilk Test Statistic: 0.9575551459470419, p-value: 0.763522912945692
# Attrition Win Rates - Shapiro-Wilk Test Statistic: 0.8313381414546486, p-value: 0.007326504903752133
# Mid-Range Win Rates - Shapiro-Wilk Test Statistic: 0.8492319354129841, p-value: 0.021683634097657948
# Classic Control Win Rates - Shapiro-Wilk Test Statistic: 0.9293309387618782, p-value: 0.21210244830350308
# Classic Aggro Win Rates - Shapiro-Wilk Test Statistic: 0.8641800383090643, p-value: 0.24364845662451412
# Normality holds.

# Perform Levene's Test
stat, p = levene(*groups)
print(f"Levene’s Test Statistic: {stat}, p-value: {p}")

# Levene’s Test Statistic: 1.1102347496364542, p-value: 0.3619139789956909 (Failed to reject)
# Data is HOMOGENEOUS

# ANOVA is valid

# Finding 2. The mean win rate is equal across all archetypes.