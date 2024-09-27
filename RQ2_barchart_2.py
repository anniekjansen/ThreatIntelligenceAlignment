import matplotlib.pyplot as plt
import numpy as np

# Define the data
data = np.array([
    [25, 25],
    [24, 24],
    [0, 24],
    [20, 20],
    [14,14],
    [9, 9]
])

# Define the row and column labels
products = ['MS Windows', 'Adobe Flash Player', 'Unknown', 'MS Internet Explorer', 'MS Office', 'Adobe AIR']
categories = ['Top 5 overall/APT', 'Top 5 NCSC']

# Create the bar chart
fig, ax = plt.subplots(figsize=(8, 6))
bar_width = 0.35
x = np.arange(len(products))

bars1 = ax.bar(x - bar_width/2, data[:, 0], bar_width, label=categories[0])
bars2 = ax.bar(x + bar_width/2, data[:, 1], bar_width, label=categories[1], color='skyblue')

for bar, vulnerability in zip(bars1, data[:, 0]):
    if vulnerability != 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, f"{vulnerability}", ha='center', va='center')

for bar, vulnerability in zip(bars2, data[:, 1]):
    if vulnerability != 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, f"{vulnerability}", ha='center', va='center')

ax.set_title('Number of Vulnerabilities by Product and Dataset')
ax.set_xlabel('Product')
ax.set_ylabel('Number of Vulnerabilities')
ax.set_xticks(x)
ax.set_xticklabels(products)
ax.legend()

plt.show()