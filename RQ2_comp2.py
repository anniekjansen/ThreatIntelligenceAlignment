import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data: Replace this with your actual data
df = pd.read_csv('query-result-6.2.csv')

df.rename(columns={
    'productName': 'Product',       # Ensure the name matches your CSV
    'vulnerabilityCount': 'Popularity', # Ensure the name matches your CSV
    'likelihoodLabel': 'Likelihood'   # Ensure the name matches your CSV
}, inplace=True)

print(df.head())

# Convert Likelihood to numeric values
likelihood_mapping = {'High': 3, 'Medium': 2, 'Low': 1}
df['Likelihood_Numeric'] = df['Likelihood'].map(likelihood_mapping)

# Optional: Chi-squared test
contingency_table = pd.crosstab(df['Product'], df['Likelihood'])
chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency_table)

print("Chi-Squared Statistic:", chi2)
print("P-Value for Chi-Squared:", p_chi2)


