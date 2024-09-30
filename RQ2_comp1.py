import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

product_df = pd.read_csv('query-result-6.1.csv')

product_df.rename(columns={
    'productName': 'product',       # Ensure the name matches your CSV
    'count': 'count', # Ensure the name matches your CSV
    'justificationType': 'justificationType'   # Ensure the name matches your CSV
}, inplace=True)

# Create a binary justification column
justification_binary = product_df['justificationType'].apply(lambda x: 'Justified' if x == 'Justified' else 'Non-Justified')

# Create a contingency table with product and binary justification
contingency_table = pd.pivot_table(product_df, index='product', columns=justification_binary, aggfunc='size', fill_value=0)

# Calculate the odds ratio for each product
odds_ratios = {}
for product in contingency_table.index:
    a = contingency_table.loc[product, 'Justified']
    b = contingency_table.loc[product, 'Non-Justified']
    c = contingency_table.loc[:, 'Justified'].sum() - a
    d = contingency_table.loc[:, 'Non-Justified'].sum() - b
    odds_ratio = (a / c) / (b / d)
    odds_ratios[product] = odds_ratio

# Print the odds ratios
print("\nOdds Ratios for Product Justification")
print(odds_ratios)

# Perform chi-squared test
chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency_table)

# Print the chi-squared test results
print("\nChi-Squared Test Result for Product Justification")
print("Chi-Squared Statistic:", chi2)
print("P-Value for Chi-Squared:", p_chi2)
