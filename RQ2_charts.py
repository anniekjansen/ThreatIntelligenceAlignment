import numpy as np

from ChartCreator import ChartCreator

""" Bar Chart 1 """
labels = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8']
vulnerabilities = [86, 24, 45, 6, 24, 0, 24, 0]
total_vulnerabilities = 86
ChartCreator().create_bar_chart(labels, vulnerabilities, 'Vulnerability Analysis', 'SPARQL Query', 'Number of Vulnerabilities', total_vulnerabilities)

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
ChartCreator().create_grouped_bar_chart(data, products, categories, 'Number of Vulnerabilities by Product and Dataset', 'Product', 'Number of Vulnerabilities', 'skyblue')

""" Bar Chart 3 """
labels = ['No Change', 'Unimportant', 'Justified', 'Unjustified']
vulnerabilities = [40, 36, 10, 9]
ChartCreator().create_bar_chart_with_custom_width(labels, vulnerabilities, 'Update Justification Analysis', 'Justification', 'Number of Vulnerabilities', 0.55, 12)

""" Bar Chart 4 """
labels = ['Low', 'Medium', 'High']
vulnerabilities = [1, 50, 63]
ChartCreator().create_bar_chart_with_custom_width(labels, vulnerabilities, 'Likelihood Analysis', 'Likelihood', 'Number of Vulnerabilities', 0.55, 12)

""" Venn Diagram """
set_a = {    "UNIX", "Red Hat", "FreeBSD", "SUSE", "BSD", "BlackBerry", "Ubuntu", 
    "HP-UX", "OpenVMS", "IBM AIX", "IBM z/OS", "Red Hat Enterprise Linux", "Windows 8"}
set_b = {"professional x64", "Windows Server 2019"}

# Define the intersection
intersection = {"Android", "Apple Mac", "Apple iOS", "Chrome OS", "Linux", "Solaris", 
    "Unknown", "Windows", "Windows 10", "Windows 7", "Windows 8.1", "Windows Server", 
    "Windows Server 2003", "Windows Server 2008", "Windows Server 2012", 
    "Windows Server 2016", "Windows Vista", "Windows XP"}
ChartCreator().create_venn_diagram(set_a, set_b, intersection)