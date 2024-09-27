import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Data for justified counts
justified_data = {
    "justificationType": ["Justified", "Non-Justified", "nan"],
    "count": [7, 76, 3]  # Example counts
}
justified_df = pd.DataFrame(justified_data)

# Likelihood vs Justification Results
likelihood_data = {
    "justificationType": ["Justified", "Justified", "Non-Justified", "Non-Justified", "Non-Justified", "nan"],
    "likelihoodType": ["High", "Medium", "High", "Low", "Medium", "High"],
    "count": [7, 7, 53, 1, 43, 3]  # Example counts
}
likelihood_df = pd.DataFrame(likelihood_data)

# Comparative Analysis
print("Comparative Risk Analysis")
print(justified_df)

# Grouping likelihood data by justification and likelihood types
likelihood_grouped = likelihood_df.groupby(['justificationType', 'likelihoodType']).sum().reset_index()

# Print the grouped likelihood data
print("\nLikelihood vs Justification Results")
print(likelihood_grouped)

# Prepare data for Chi-Squared Test
# We will compare justified and non-justified counts for high likelihood cases
high_counts = likelihood_grouped[likelihood_grouped['likelihoodType'] == "High"]

# If there are any nan values, we can exclude them from the chi-squared test
high_counts = high_counts[high_counts['justificationType'] != "nan"]

# Split justified and non-justified counts for the chi-squared test
justified_high_count = high_counts[high_counts['justificationType'] == "Justified"]['count'].values
non_justified_high_count = high_counts[high_counts['justificationType'] == "Non-Justified"]['count'].values

# Handle missing counts
if justified_high_count.size == 0:
    justified_high_count = [0]
if non_justified_high_count.size == 0:
    non_justified_high_count = [0]

# Combine into a single observed frequency list
observed_counts = [justified_high_count[0], non_justified_high_count[0]]

# Calculate total for expected frequencies
total_observed = sum(observed_counts)

# Set expected counts to be evenly distributed (assuming equal risk)
expected_counts = [total_observed / 2, total_observed / 2]

# Perform Chi-Squared Test
chi2_stat, p_val = stats.chisquare(f_obs=observed_counts, f_exp=expected_counts)

# Output Chi-Squared Test Results
print("\nChi-Squared Test Result for High Likelihood")
print(f"Chi2 Stat: {chi2_stat}, P-Value: {p_val}")




# Set the aesthetics for the plots
sns.set(style="whitegrid")

# Create a bar plot for likelihood vs justification
plt.figure(figsize=(10, 6))
sns.barplot(x='likelihoodType', y='count', hue='justificationType', data=likelihood_df)

plt.title('Distribution of Justified and Non-Justified Vulnerabilities by Likelihood')
plt.xlabel('Likelihood Type')
plt.ylabel('Count')
plt.legend(title='Justification Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



