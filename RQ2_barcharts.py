import matplotlib.pyplot as plt
import numpy as np

from BarChartCreator import BarChartCreator

""" Bar Chart 1 """
# Create bar charts
labels = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8']
vulnerabilities = [86, 24, 45, 6, 24, 0, 24, 0]
total_vulnerabilities = 86
BarChartCreator().create_bar_chart(labels, vulnerabilities, 'Vulnerability Analysis', 'SPARQL Query', 'Number of Vulnerabilities', total_vulnerabilities)

""" Bar Chart 2 """
data = np.array([
    [25, 25],
    [24, 24],
    [0, 24],
    [20, 20],
    [14,14],
    [9, 9]
])
products = ['MS Windows', 'Adobe Flash Player', 'Unknown', 'MS Internet Explorer', 'MS Office', 'Adobe AIR']
categories = ['Top 5 overall/APT', 'Top 5 NCSC']
BarChartCreator().create_grouped_bar_chart(data, products, categories, 'Number of Vulnerabilities by Product and Dataset', 'Product', 'Number of Vulnerabilities', 'skyblue')

""" Bar Chart 3 """
labels = ['No Change', 'Unimportant', 'Justified', 'Unjustified']
vulnerabilities = [40, 36, 10, 9]
BarChartCreator().create_bar_chart_with_custom_width(labels, vulnerabilities, 'Update Justification Analysis', 'Justification', 'Number of Vulnerabilities', 0.55, 12)

""" Bar Chart 4 """
labels = ['Low', 'Medium', 'High']
vulnerabilities = [1, 50, 63]
BarChartCreator().create_bar_chart_with_custom_width(labels, vulnerabilities, 'Likelihood Analysis', 'Likelihood', 'Number of Vulnerabilities', 0.55, 12)
