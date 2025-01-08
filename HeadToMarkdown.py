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

print(df_c.head().to_markdown(index=False))
print(df_q.head().to_markdown(index=False))