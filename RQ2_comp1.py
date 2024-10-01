import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

product_df = pd.read_csv('query-result-6.1.csv')

# Create a binary justification column
justification_binary = product_df['justificationType'].apply(lambda x: 'Justified' if x == 'Justified' else 'Non-Justified')

# Create a contingency table with product and binary justification
contingency_table = pd.pivot_table(product_df, index='productName', columns=justification_binary, aggfunc='size', fill_value=0)

# Calculate the odds ratio for each product
odds_ratios = {}
for product in contingency_table.index:
    a = contingency_table.loc[product, 'Justified']
    b = contingency_table.loc[product, 'Non-Justified']
    c = contingency_table.loc[:, 'Justified'].sum() - a
    d = contingency_table.loc[:, 'Non-Justified'].sum() - b
    
    # Check for division by zero
    if c == 0 or d == 0:
        odds_ratio = np.nan
    else:
        odds_ratio = (a / c) / (b / d)
    
    odds_ratios[product] = odds_ratio

# Create a dataframe with the odds ratios
odds_ratios_df = pd.DataFrame(list(odds_ratios.items()), columns=['Product', 'Odds_Ratio'])

# Print the odds ratios
print("\nOdds Ratios for Product Justification")
print(odds_ratios_df)

# Print the top 5 highest odds ratio
print("\nTop 5 Highest Odds Ratio:")
print(odds_ratios_df.sort_values(by='Odds_Ratio', ascending=False).dropna().head(5))

# Print the top 5 lowest odds ratio
print("\nTop 5 Lowest Odds Ratio:")
print(odds_ratios_df.sort_values(by='Odds_Ratio', ascending=True).dropna().head(5))

# Perform chi-squared test
chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency_table)

# Print the chi-squared test results
print("\nChi-Squared Test Result for update justification per product")
print("Chi-Squared Statistic:", chi2)
print("P-Value for Chi-Squared:", p_chi2)
