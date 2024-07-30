import pandas as pd
import string
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from URREFHelper import URREFHelper

""" Load datasets """
ncsc_data = DataLoaderSaver().load_dataset("NCSC", "engineered")
apt_data = DataLoaderSaver().load_dataset("APT", "processed")
ncsc_classification_data = DataLoaderSaver().load_dataset("NCSC", "classification")

""" Explode NCSC datasets so each CVE-ID is its own instance """
ncsc_data = URREFHelper().explode_columns(ncsc_data, ['CVE-ID'])
ncsc_classification_data = URREFHelper().explode_columns(ncsc_classification_data, ['CVE-ID'])

ncsc_data['Uitgiftedatum'] = pd.to_datetime(ncsc_data['Uitgiftedatum'], utc=True)

# print(f"Number of unique CVE-IDs NCSC: {len(ncsc_data['CVE-ID'].unique())}")
# print(f"Number of unique CVE-IDs APT: {len(apt_data['CVE-ID'].unique())}")

ncsc = ncsc_data[["CVE-ID", "Uitgiftedatum", "Update", "Kans"]]
apt = apt_data[['CVE-ID','reserved_time', "published_time", "exploited_time"]]

""" Merge NCSC and APT datasets """
merged = pd.merge(ncsc, apt, on='CVE-ID')

""" Convert Uitgiftedatum to the first day of the month """
merged['Uitgiftedatum'] = merged['Uitgiftedatum'].dt.to_period('M').dt.to_timestamp()
merged['Uitgiftedatum'] = merged['Uitgiftedatum'].dt.tz_localize('UTC')

""" RQ 1.1 """
time_columns = ['Uitgiftedatum', 'reserved_time', 'published_time', 'exploited_time']

# Convert datetime objects to Unix timestamps
merged['Uitgiftedatum_unix'] = merged['Uitgiftedatum'].apply(lambda x: x.timestamp())
merged['reserved_time_unix'] = merged['reserved_time'].apply(lambda x: x.timestamp())
merged['exploited_time_unix'] = merged['exploited_time'].apply(lambda x: x.timestamp())

# Compare reserved_time with Uitgiftedatum of initial NCSC (Update 1)
update_1_data = merged[merged['Update'] == 1][['reserved_time_unix', 'Uitgiftedatum_unix']]
update_1_corr_coef, update_1_p_value = stats.pearsonr(update_1_data['reserved_time_unix'], update_1_data['Uitgiftedatum_unix'])

print("Correlation between reserved_time and Uitgiftedatum for Update 1:")
print(f"Correlation Coefficient: {update_1_corr_coef:.4f}")
print(f"P-value: {update_1_p_value:.4f}")

# Scatter plot
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Uitgiftedatum', y='reserved_time', data=merged[merged['Update'] == 1])
plt.title('Reserved Time vs Uitgiftedatum for Update 1')
plt.show()

mae_update_1 = np.mean(np.abs(merged[merged['Update'] == 1]['reserved_time'] - merged[merged['Update'] == 1]['Uitgiftedatum']))
print("MAE for Update 1:", mae_update_1)

""" RQ 1.2 """
# Compare exploited_time with Uitgiftedatum of NCSC updates (Update 2 and up)
update_gt_1_data = merged[merged['Update'] > 1][['exploited_time_unix', 'Uitgiftedatum_unix']]
update_gt_1_corr_coef, update_gt_1_p_value = stats.pearsonr(update_gt_1_data['exploited_time_unix'], update_gt_1_data['Uitgiftedatum_unix'])

print("Correlation between exploited_time and Uitgiftedatum for Update 2 and up:")
print(f"Correlation Coefficient: {update_gt_1_corr_coef:.4f}")
print(f"P-value: {update_gt_1_p_value:.4f}")

# Scatter plot
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Uitgiftedatum', y='exploited_time', data=merged[merged['Update'] > 1])
plt.title('Exploited Time vs Uitgiftedatum for Update 2 and up')
plt.show()

mae_update_gt_1 = np.mean(np.abs(merged[merged['Update'] > 1]['exploited_time'] - merged[merged['Update'] > 1]['Uitgiftedatum']))
print("MAE for Update 2 and up:", mae_update_gt_1)

""" RQ 1.3 """
merged = pd.merge(ncsc, apt, on='CVE-ID')
ncsc_classification_data.rename(columns = {'Kans justified+important change':'Justified'}, inplace = True)
ncsc_classification_data = ncsc_classification_data[['CVE-ID', 'Justified']]

merged = pd.merge(merged, ncsc_classification_data, on='CVE-ID')
# print(merged.head())

# Calculate time difference from Uitgiftedatum to exploited_time
merged['Uitgiftedatum_to_exploited'] = (merged['exploited_time'] - merged['Uitgiftedatum']).dt.days

# Filter the data to ensure 'Justified' column contains only 0 and 1
assert set(merged['Justified'].unique()).issubset({0, 1}), "Unexpected values in 'Justified' column"

# Separate data for justified and non-justified
justified_exploited = merged.loc[merged['Justified'] == 1, 'Uitgiftedatum_to_exploited'].dropna()
non_justified_exploited = merged.loc[merged['Justified'] == 0, 'Uitgiftedatum_to_exploited'].dropna()

# Correlation analysis
correlation_coefficient, p_value_corr = stats.pearsonr(merged['Justified'], merged['Uitgiftedatum_to_exploited'])
print(f"Pearson correlation coefficient: {correlation_coefficient}, P-value: {p_value_corr}")

# Statistical test: t-test between justified and non-justified for Uitgiftedatum to exploited_time
t_stat, p_value = stats.ttest_ind(justified_exploited, non_justified_exploited, equal_var=False)
print(f"T-statistic (Uitgiftedatum to exploited_time): {t_stat}, P-value: {p_value}")


""" RQ 1.3 """
# Drop rows with missing values in relevant columns
merged_chance = merged.dropna(subset=['Uitgiftedatum_to_exploited', 'Kans'])

# Correlation analysis
if len(merged_chance) > 0:
    correlation_coefficient, p_value = stats.pearsonr(
        merged_chance['Uitgiftedatum_to_exploited'],
        pd.factorize(merged_chance['Kans'])[0]  # Convert categories to numerical
    )
    print(f"Pearson correlation coefficient: {correlation_coefficient}, P-value: {p_value}")
else:
    print("No valid data for correlation analysis.")

# Statistical test: ANOVA or Kruskal-Wallis test (if non-normal distribution)
if len(merged_chance) > 0:
    anova_result = stats.f_oneway(
        merged_chance.loc[merged_chance['Kans'] == 'Low', 'Uitgiftedatum_to_exploited'],
        merged_chance.loc[merged_chance['Kans'] == 'Medium', 'Uitgiftedatum_to_exploited'],
        merged_chance.loc[merged_chance['Kans'] == 'High', 'Uitgiftedatum_to_exploited']
    )
    print(f"ANOVA F-statistic: {anova_result.statistic}, P-value: {anova_result.pvalue}")
else:
    print("No valid data for statistical test.")





# # Visualization: Box plot for Uitgiftedatum to exploited_time
# sns.boxplot(x='Justified', y='Uitgiftedatum_to_exploited', data=merged)
# plt.title('Justified vs Uitgiftedatum to Exploited Time')
# plt.show()

# # Calculate z-scores for Uitgiftedatum to exploited_time
# merged['zscore'] = stats.zscore(merged['Uitgiftedatum_to_exploited'])

# # Identify outliers using z-score (typically |z-score| > 3 is considered an outlier)
# outliers = merged[abs(merged['zscore']) > 5]

# # Count outliers by 'Justified' and 'Non-Justified'
# justified_outliers = outliers[outliers['Justified'] == 1]
# non_justified_outliers = outliers[outliers['Justified'] == 0]

# # Summary of outliers by classification
# print("Total number of outliers:", len(outliers))
# print("\nOutliers details:")
# print(outliers[['CVE-ID', 'Uitgiftedatum_to_exploited', 'Justified', 'zscore']])

# # Print counts of justified and non-justified outliers
# print("\nCount of Justified outliers:", len(justified_outliers))
# print("Count of Non-Justified outliers:", len(non_justified_outliers))