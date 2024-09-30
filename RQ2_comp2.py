import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('query-result-6.2.csv')

df.rename(columns={
    'productName': 'Product',       # Ensure the name matches your CSV
    'vulnerabilityCount': 'Popularity', # Ensure the name matches your CSV
    'likelihoodLabel': 'Likelihood'   # Ensure the name matches your CSV
}, inplace=True)

# print(df.head())

# Convert Likelihood to numeric values
likelihood_mapping = {'High': 3, 'Medium': 2, 'Low': 1}
df['Likelihood_Numeric'] = df['Likelihood'].map(likelihood_mapping)

# Create a binary likelihood column
likelihood_binary = df['Likelihood'].apply(lambda x: 'High' if x == 'High' else 'Low/Medium')

# Create a contingency table with binary likelihood and product
contingency_table = pd.crosstab(likelihood_binary, df['Product'])

# Perform chi-squared test
chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency_table)

print("Chi-Squared Statistic:", chi2)
print("P-Value for Chi-Squared:", p_chi2)

# Create a contingency table with likelihood and popularity
contingency_table = pd.crosstab(likelihood_binary, df['Product'], values=df['Popularity'], aggfunc='sum')

# Calculate the odds ratio for each product
odds_ratios = {}
for product in contingency_table.columns:
    a = contingency_table.loc['High', product]
    b = contingency_table.loc['Low/Medium', product]
    c = contingency_table.loc['High'].sum() - a
    d = contingency_table.loc['Low/Medium'].sum() - b
    odds_ratio = (a / c) / (b / d)
    odds_ratios[product] = odds_ratio

# Add the odds ratios to the original dataframe
df['Odds_Ratio'] = df['Product'].map(odds_ratios)

# Print the updated dataframe
print(df)

