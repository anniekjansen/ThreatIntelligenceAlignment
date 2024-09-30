import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

likelihood_df = pd.read_csv('query-result-6.3.csv')

likelihood_df.rename(columns={
    'justificationType': 'justificationType',       # Ensure the name matches your CSV
    'count': 'count', # Ensure the name matches your CSV
    'likelihoodType': 'likelihoodType'   # Ensure the name matches your CSV
}, inplace=True)

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
    odds_ratio = (a / c) / (b / d)
    odds_ratios[justification] = odds_ratio

# Print the odds ratios
print("\nOdds Ratios for High Likelihood per Update Justification")
print(odds_ratios)

# Perform chi-squared test
chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency_table)

# Print the chi-squared test results
print("\nChi-Squared Test Result for High Likelihood per Update Justification")
print("Chi-Squared Statistic:", chi2)
print("P-Value for Chi-Squared:", p_chi2)

# Bar chart of odds ratios
plt.figure(figsize=(10, 6))
sns.barplot(x=list(odds_ratios.keys()), y=list(odds_ratios.values()))
plt.title('Odds Ratios for High Likelihood per Update Justification')
plt.xlabel('Justification Type')
plt.ylabel('Odds Ratio')
plt.show()

# Heatmap of contingency table
plt.figure(figsize=(10, 6))
sns.heatmap(contingency_table, annot=True, cmap='Blues')
plt.title('Contingency Table of Justification Type vs. Likelihood')
plt.xlabel('Justification Type')
plt.ylabel('Likelihood')
plt.show()




