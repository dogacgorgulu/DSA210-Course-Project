import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
from scipy.stats import levene
import seaborn as sns
from pingouin import welch_anova



# df_c tonly includes categorical data
df_c = pd.read_excel("data/ArenaData_categorical.xlsx")

# df_q only includes quanitative data
df_q = pd.read_excel("data/ArenaData_quantitative.xlsx")

# Calculate winrates
df_c['Win Rate'] = df_c['W'] / df_c['Total Matches']
df_q['Win Rate'] = df_q['W'] / df_q['Total Matches']

print(df_c.head())
print(df_q.head())

# H_0: The mean Win Rate is the same for all Classes (FAILED TO REJECT)
# Group win rates by class
groups = [df_c[df_c['Class'] == cls]['Win Rate'] for cls in df_c['Class'].unique()]
# Perform ANOVA
f_stat, p_val = f_oneway(*groups)
print(f"ANOVA F-statistic: {f_stat}, p-value: {p_val}")

# F-statistic: 0.6326618402826653, p-value: 0.7780008552299287

######################
# H_0: The mean Win Rate is the same for all Archetypes (FAILED TO REJECT)
# Group win rates by Archetype
groups = [df_c[df_c['Archetype'] == archetype]['Win Rate'] for archetype in df_c['Archetype'].unique()]
# Perform ANOVA
f_stat, p_val = f_oneway(*groups)
print(f"ANOVA F-statistic: {f_stat}, p-value: {p_val}")
# F-statistic: 1.044284028884457, p-value: 0.3936552667822725
#######################

print(df_c.groupby('Class')['Win Rate'].var())
print(df_c.groupby('Archetype')['Win Rate'].var())

# Test for variance equality among Classes
stat, p_val = levene(*[df_c[df_c['Class'] == cls]['Win Rate'] for cls in df_c['Class'].unique()])
print(f"Levene’s Test Statistic: {stat}, p-value: {p_val}")
# Levene’s Test Statistic: 0.8219981373712096, p-value: 0.6095329149643589
# Variances of Win Rate across the groups (e.g., Class or Archetype) are not significantly different
# ANOVA is not violated



# Group by Class and sum Wins, Losses, and Total Matches
class_summary = df_c.groupby('Class').agg({
    'W': 'sum',             # Total wins for each class
    'L': 'sum',             # Total losses for each class
    'Total Matches': 'sum'  # Total matches for each class
}).reset_index()

# Calculate Win Rate for each class
class_summary['Win Rate'] = class_summary['W'] / class_summary['Total Matches']



# Display the class-level summary
print(class_summary)

# Perform ANOVA on aggregated win rates
groups = [df_c[df_c['Class'] == cls]['Win Rate'] for cls in df_c['Class'].unique()]
f_stat, p_val = f_oneway(*groups)

print(f"ANOVA F-statistic: {f_stat}, p-value: {p_val}")

# ANOVA F-statistic: 0.6326618402826653, p-value: 0.7780008552299287
# p > 0.05
# Fail to reject the null hypothesis 
# Indicates no significant differences in win rates between the Class groups.


# Bar plot of aggregated Win Rates by Class
sns.barplot(data=class_summary, x='Class', y='Win Rate', palette='pastel')
plt.title('Aggregated Win Rate by Class')
plt.xticks(rotation=45)
plt.ylabel('Win Rate')
plt.show()

# Group by Archetype and sum Wins, Losses, and Total Matches
archetype_summary = df_c.groupby('Archetype').agg({
    'W': 'sum',             # Total wins for each archetype
    'L': 'sum',             # Total losses for each archetype
    'Total Matches': 'sum'  # Total matches for each archetype
}).reset_index()

# Calculate Win Rate for each archetype
archetype_summary['Win Rate'] = archetype_summary['W'] / archetype_summary['Total Matches']

# Display the archetype-level summary
print(archetype_summary)

# Perform ANOVA on aggregated win rates
groups = [df_c[df_c['Archetype'] == archetype]['Win Rate'] for archetype in df_c['Archetype'].unique()]
f_stat, p_val = f_oneway(*groups)

print(f"ANOVA F-statistic: {f_stat}, p-value: {p_val}")

# Bar plot of aggregated Win Rates by Archetype
sns.barplot(data=archetype_summary, x='Archetype', y='Win Rate', palette='pastel')
plt.title('Aggregated Win Rate by Archetype')
plt.xticks(rotation=45)
plt.ylabel('Win Rate')
plt.show()

# ANOVA F-statistic: 1.044284028884457, p-value: 0.3936552667822725
# p > 0.05
# Fail to reject the null hypothesis 
# Indicates no significant differences in win rates between the Archetype groups.

import scipy.stats as stats
import matplotlib.pyplot as plt

# Normality Test for Class Summary
stats.probplot(class_summary['Win Rate'], dist="norm", plot=plt)
plt.title("Q-Q Plot for Class Win Rates")
plt.show()

stat, p = stats.shapiro(class_summary['Win Rate'])
print(f"Class Win Rates - Shapiro-Wilk Test Statistic: {stat}, p-value: {p}")

# Normality Test for Archetype Summary
stats.probplot(archetype_summary['Win Rate'], dist="norm", plot=plt)
plt.title("Q-Q Plot for Archetype Win Rates")
plt.show()

stat, p = stats.shapiro(archetype_summary['Win Rate'])
print(f"Archetype Win Rates - Shapiro-Wilk Test Statistic: {stat}, p-value: {p}")

# Levene's Test for Class
stat, p = levene(class_summary['Win Rate'], [1] * len(class_summary))
print(f"Class Win Rates - Levene’s Test Statistic: {stat}, p-value: {p}")
# p-value: 0.006084786932541696
# NOT HOMOGENEOUS
# CONSIDER Welch's ANOVA

# Levene's Test for Archetype
stat, p = levene(archetype_summary['Win Rate'], [1] * len(archetype_summary))
print(f"Archetype Win Rates - Levene’s Test Statistic: {stat}, p-value: {p}")

# Welch's ANOVA for Class
welch_results_class = welch_anova(data=class_summary, dv='Win Rate', between='Class')
print(welch_results_class)
# f-statistic = 0, p-value = 1 A PROBLEM 
# CONSIDER 

print(class_summary)

print(class_summary.groupby('Class')['Win Rate'].var())
