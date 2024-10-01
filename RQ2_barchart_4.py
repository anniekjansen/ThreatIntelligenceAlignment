import matplotlib.pyplot as plt

labels = ['Low', 'Medium', 'High']
vulnerabilities = [1, 50, 63]
# total_vulnerabilities = 86

fig, ax = plt.subplots(figsize=(5, 5))
bar_width = 0.55  # adjust the width of the bars
bar_plot = ax.bar(labels, vulnerabilities, width=bar_width)

for bar, vulnerability in zip(bar_plot, vulnerabilities):
    if vulnerability != 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, f"{vulnerability}", ha='center', va='center', fontsize=12)

# for bar, vulnerability in zip(bar_plot, vulnerabilities):
#     percentage = (vulnerability / total_vulnerabilities) * 100
#     ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3, f"({percentage:.1f}%)", ha='center', va='bottom', fontsize=9)

ax.set_title('Likelihood Analysis')
ax.set_xlabel('Likelihood')
ax.set_ylabel('Number of Vulnerabilities')

ax.set_ylim(0, max(vulnerabilities) * 1.1)
plt.show()