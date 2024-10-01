import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class CompAnalyzer:

    def calculate_odds_ratios(self, contingency_table, index_name, column_name):
        if index_name in contingency_table.index:
            odds_ratios = {}
            for column in contingency_table.columns:
                a = contingency_table.loc[index_name, column]
                b = contingency_table.loc[contingency_table.index[contingency_table.index != index_name][0], column]
                c = contingency_table.loc[index_name].sum() - a
                d = contingency_table.loc[contingency_table.index[contingency_table.index != index_name][0]].sum() - b
                
                # Check for division by zero
                if c == 0 or d == 0:
                    odds_ratio = np.nan  # or some other default value
                else:
                    odds_ratio = (a / c) / (b / d)
                
                odds_ratios[column] = odds_ratio
            
            return odds_ratios
        elif index_name in contingency_table.columns:
            odds_ratios = {}
            for index in contingency_table.index:
                a = contingency_table.loc[index, index_name]
                b = contingency_table.loc[index, column_name]
                c = contingency_table.loc[:, index_name].sum() - a
                d = contingency_table.loc[:, column_name].sum() - b
                
                # Check for division by zero
                if c == 0 or d == 0:
                    odds_ratio = np.nan  # or some other default value
                else:
                    odds_ratio = (a / c) / (b / d)
                
                odds_ratios[index] = odds_ratio
            
            return odds_ratios
        else:
            return None

    def perform_chi_squared_test(self, contingency_table):
        chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency_table)
        return chi2, p_chi2, dof

    def print_results(self, odds_ratios, chi2, p_chi2, dof):
        print("\nOdds Ratios:")
        print(odds_ratios)
        
        print("\nTop 5 Highest Odds Ratio:")
        print(pd.DataFrame(list(odds_ratios.items()), columns=['Column', 'Odds_Ratio']).sort_values(by='Odds_Ratio', ascending=False).dropna().head(5).reset_index(drop=True))
        
        print("\nTop 5 Lowest Odds Ratio:")
        print(pd.DataFrame(list(odds_ratios.items()), columns=['Column', 'Odds_Ratio']).sort_values(by='Odds_Ratio', ascending=True).dropna().head(5).reset_index(drop=True))
        
        print("\nChi-Squared Test Results:")
        print("Chi-Squared Statistic:", chi2)
        print("P-Value for Chi-Squared:", p_chi2)
        print("Degrees of Freedom:", dof)

    def create_heatmap_contingency(self, contingency_table):
        plt.figure(figsize=(10, 6))
        sns.heatmap(contingency_table, annot=True, cmap='Blues')
        plt.title('Contingency Table of Justification Type vs. Likelihood')
        plt.xlabel('Justification Type')
        plt.ylabel('Likelihood')
        plt.show()