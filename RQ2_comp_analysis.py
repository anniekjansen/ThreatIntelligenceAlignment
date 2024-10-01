import pandas as pd

from CompAnalyzer import CompAnalyzer

""" 6.1 """
product_df = pd.read_csv('./SPARQL Queries/Results/query-result-6.1.csv')
justification_binary = product_df['justificationType'].apply(lambda x: 'Justified' if x == 'Justified' else 'Non-Justified')
contingency_table = pd.pivot_table(product_df, index='productName', columns=justification_binary, aggfunc='size', fill_value=0)
odds_ratios = CompAnalyzer().calculate_odds_ratios(contingency_table, 'Justified', 'Non-Justified')
chi2, p_chi2, dof = CompAnalyzer().perform_chi_squared_test(contingency_table)
CompAnalyzer().print_results(odds_ratios, chi2, p_chi2, dof)

""" 6.2 """
df = pd.read_csv('./SPARQL Queries/Results/query-result-6.2.csv')
likelihood_binary = df['likelihoodLabel'].apply(lambda x: 'High' if x == 'High' else 'Low/Medium')
contingency_table = pd.crosstab(likelihood_binary, df['productName'])
chi2, p_chi2, dof = CompAnalyzer().perform_chi_squared_test(contingency_table)
contingency_table_odds = pd.crosstab(likelihood_binary, df['productName'], values=df['count'], aggfunc='sum')
odds_ratios = CompAnalyzer().calculate_odds_ratios(contingency_table_odds, 'High', 'Low/Medium')
CompAnalyzer().print_results(odds_ratios, chi2, p_chi2, dof)

""" 6.3 """
likelihood_df = pd.read_csv('./SPARQL Queries/Results/query-result-6.3.csv')
likelihood_binary = likelihood_df['likelihoodType'].apply(lambda x: 'High' if x == 'High' else 'Low/Medium')
contingency_table = pd.crosstab(likelihood_binary, likelihood_df['justificationType'], values=likelihood_df['count'], aggfunc='sum')
odds_ratios = CompAnalyzer().calculate_odds_ratios(contingency_table, 'High', 'Low/Medium')
chi2, p_chi2, dof = CompAnalyzer().perform_chi_squared_test(contingency_table)
CompAnalyzer().print_results(odds_ratios, chi2, p_chi2, dof)
CompAnalyzer().create_heatmap_contingency(contingency_table)
