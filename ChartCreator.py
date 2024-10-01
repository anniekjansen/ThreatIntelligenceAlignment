import matplotlib.pyplot as plt
import numpy as np
from matplotlib_venn import venn2

class ChartCreator:

    def create_bar_chart(self, labels, vulnerabilities, title, xlabel, ylabel, total_vulnerabilities=None, color=None, fontsize=10):
        fig, ax = plt.subplots(figsize=(8*0.65, 6))
        bar_plot = ax.bar(labels, vulnerabilities, color=color)

        for bar, vulnerability in zip(bar_plot, vulnerabilities):
            if vulnerability != 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, f"{vulnerability}", ha='center', va='center', fontsize=fontsize)

        if total_vulnerabilities is not None:
            for bar, vulnerability in zip(bar_plot, vulnerabilities):
                percentage = (vulnerability / total_vulnerabilities) * 100
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3, f"({percentage:.1f}%)", ha='center', va='bottom', fontsize=fontsize)

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        ax.set_ylim(0, max(vulnerabilities) * 1.1)
        plt.show()

    def create_grouped_bar_chart(self, data, products, categories, title, xlabel, ylabel, color=None):
        fig, ax = plt.subplots(figsize=(8, 6))
        bar_width = 0.35
        x = np.arange(len(products))

        bars1 = ax.bar(x - bar_width/2, data[:, 0], bar_width, label=categories[0])
        bars2 = ax.bar(x + bar_width/2, data[:, 1], bar_width, label=categories[1], color=color)

        for bar, vulnerability in zip(bars1, data[:, 0]):
            if vulnerability != 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, f"{vulnerability}", ha='center', va='center')

        for bar, vulnerability in zip(bars2, data[:, 1]):
            if vulnerability != 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, f"{vulnerability}", ha='center', va='center')

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(products)
        ax.legend()

        plt.show()

    def create_bar_chart_with_custom_width(self, labels, vulnerabilities, title, xlabel, ylabel, width, fontsize=10):
        fig, ax = plt.subplots(figsize=(5, 5))
        bar_plot = ax.bar(labels, vulnerabilities, width=width)

        for bar, vulnerability in zip(bar_plot, vulnerabilities):
            if vulnerability != 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, f"{vulnerability}", ha='center', va='center', fontsize=fontsize)

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        ax.set_ylim(0, max(vulnerabilities) * 1.1)
        plt.show()
    
    def create_venn_diagram(self, set_a, set_b, intersection):
        set_a.update(intersection)
        set_b.update(intersection)
        set_a_unique = set_a - set_b
        set_b_unique = set_b - set_a

        plt.figure(figsize=(10, 8))
        equal_size = max(len(set_a_unique), len(set_b_unique), len(intersection))

        v = venn2(subsets=(equal_size, equal_size, len(intersection)), 
                set_labels=('NCSC', 'APT'), alpha=0.5)

        v.get_patch_by_id('10').set_facecolor('#1f77b4')
        v.get_patch_by_id('01').set_facecolor('#007acc')
        v.get_patch_by_id('11').set_facecolor('skyblue') 

        label = v.get_label_by_id('10')
        label.set_text('\n'.join(set_a_unique))
        label.set_fontsize(9)

        label = v.get_label_by_id('01')
        label.set_text('\n'.join(set_b_unique))
        label.set_fontsize(9)

        label = v.get_label_by_id('11')
        label.set_text('\n'.join(intersection))
        label.set_fontsize(9)

        plt.show()