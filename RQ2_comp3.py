import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

likelihood_df = pd.read_csv('query-result-6.3.csv')

# Create a binary likelihood column
likelihood_binary = likelihood_df['likelihoodType'].apply(lambda x: 'High' if x == 'High' else 'Low/Medium')

# Create a contingency table with justification type and binary likelihood
contingency_table = pd.crosstab(likelihood_binary, likelihood_df['justificationType'], values=likelihood_df['count'], aggfunc='sum')

# Calculate the odds ratio for each justification type
odds_ratios = {}
for justification in contingency_table.columns:
    a = contingency_table.loc['High', justification]
    b = contingency_table.loc['Low/Medium', justification]
    c = contingency_table.loc['High'].sum() - a
    d = contingency_table.loc['Low/Medium'].sum() - b
    
    # Check for division by zero
    if c == 0 or d == 0:
        odds_ratio = np.nan
    else:
        odds_ratio = (a / c) / (b / d)
    
    odds_ratios[justification] = odds_ratio

# Create a dataframe with the odds ratios
odds_ratios_df = pd.DataFrame(list(odds_ratios.items()), columns=['Justification', 'Odds_Ratio'])

# Print the odds ratios
print("\nOdds Ratios for High Likelihood per Update Justification")
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
print("\nChi-Squared Test Result for High likelihood per justification")
print("Chi-Squared Statistic:", chi2)
print("P-Value for Chi-Squared:", p_chi2)

# Heatmap of contingency table
plt.figure(figsize=(10, 6))
sns.heatmap(contingency_table, annot=True, cmap='Blues')
plt.title('Contingency Table of Justification Type vs. Likelihood')
plt.xlabel('Justification Type')
plt.ylabel('Likelihood')
plt.show()