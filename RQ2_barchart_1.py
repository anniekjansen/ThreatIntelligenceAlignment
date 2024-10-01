import matplotlib.pyplot as plt

labels = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8']
vulnerabilities = [86, 24, 45, 6, 24, 0, 24, 0]
total_vulnerabilities = 86

fig, ax = plt.subplots(figsize=(8*0.65, 6))
bar_plot = ax.bar(labels, vulnerabilities)

for bar, vulnerability in zip(bar_plot, vulnerabilities):
    if vulnerability != 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, f"{vulnerability}", ha='center', va='center')

for bar, vulnerability in zip(bar_plot, vulnerabilities):
    percentage = (vulnerability / total_vulnerabilities) * 100
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3, f"({percentage:.1f}%)", ha='center', va='bottom', fontsize=9)

ax.set_title('Vulnerability Analysis')
ax.set_xlabel('SPARQL Query')
ax.set_ylabel('Number of Vulnerabilities')

ax.set_ylim(0, max(vulnerabilities) * 1.1)
plt.show()