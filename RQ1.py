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

merged['Uitgiftedatum_to_exploited'] = (merged['exploited_time'] - merged['Uitgiftedatum']).dt.days

justified_exploited = merged.loc[merged['Justified'] == 1, 'Uitgiftedatum_to_exploited'].dropna()
non_justified_exploited = merged.loc[merged['Justified'] == 0, 'Uitgiftedatum_to_exploited'].dropna()

# Correlation analysis
correlation_coefficient, p_value_corr = stats.pearsonr(merged['Justified'], merged['Uitgiftedatum_to_exploited'])
print(f"Pearson correlation coefficient: {correlation_coefficient}, P-value: {p_value_corr:.4f}")

# Statistical test: t-test between justified and non-justified for Uitgiftedatum to exploited_time
t_stat, p_value = stats.ttest_ind(justified_exploited, non_justified_exploited, equal_var=False)
print(f"T-statistic (Uitgiftedatum to exploited_time): {t_stat}, P-value: {p_value:.4f}")

# plt.figure(figsize=(8, 6))
# plt.scatter(merged['Justified'], merged['Uitgiftedatum_to_exploited'])
# plt.xlabel('Justified (0 or 1)')
# plt.ylabel('Time difference (Uitgiftedatum to exploited)')
# plt.title('Scatterplot of Justified vs. Time difference')
# plt.show()

plt.figure(figsize=(7, 6))
plt.boxplot([justified_exploited, non_justified_exploited], patch_artist=True, medianprops=dict(color="black"))
plt.xlabel('Justification')
plt.ylabel('Time difference (in days)')
plt.title('Boxplot Justification vs. Time Differences')
plt.xticks([1, 2], ['Justified', 'Non-Justified'])
plt.show()

""" RQ 1.4 """
# Correlation analysis
correlation_coefficient, p_value = stats.pearsonr(merged['Uitgiftedatum_to_exploited'],pd.factorize(merged['Kans'])[0])  # Convert categories to numerical
print(f"Pearson correlation coefficient: {correlation_coefficient}, P-value: {p_value:.4f}")

# Statistical test: ANOVA or Kruskal-Wallis test (if non-normal distribution)
anova_result = stats.f_oneway(
        merged.loc[merged['Kans'] == 'Low', 'Uitgiftedatum_to_exploited'],
        merged.loc[merged['Kans'] == 'Medium', 'Uitgiftedatum_to_exploited'],
        merged.loc[merged['Kans'] == 'High', 'Uitgiftedatum_to_exploited']
    )
print(f"ANOVA F-statistic: {anova_result.statistic}, P-value: {anova_result.pvalue:.4f}")


# plt.figure(figsize=(8, 6))
# plt.scatter(pd.factorize(merged['Kans'])[0], merged['Uitgiftedatum_to_exploited'])
# plt.xlabel('Kans (Low, Medium, High)')
# plt.ylabel('Time difference (Uitgiftedatum to exploited)')
# plt.title('Scatterplot of Kans vs. Time difference')
# plt.show()

m = merged.groupby('Kans')['Uitgiftedatum_to_exploited'].apply(list)
name_sort = {'Low':0,'Medium':1,'High':2}
m = m.rename(index=name_sort)

plt.figure(figsize=(7, 6))
plt.boxplot(m.values.tolist(), patch_artist=True, medianprops=dict(color="black"))
plt.xlabel('Likelihood')
plt.ylabel('Time Differences (in days)')
plt.title('Boxplot of Likelihood vs. Time Differences')
plt.xticks([1, 2, 3], ['Low', 'Medium', 'High'])
plt.show()

""" Save intermediate dataset """
security_dataset = "merged"
DataLoaderSaver().save_dataset(merged, security_dataset, "merged")