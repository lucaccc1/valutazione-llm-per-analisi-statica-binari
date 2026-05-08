import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def genera(df, output_dir):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Inlined_Count', y='LLM Judge', hue='Model', palette='rocket', marker='o', errorbar=None, linewidth=2.5, markersize=8)
    plt.title("Impact of Inter-procedural Context on Accuracy", fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Average Accuracy (LLM Judge)')
    plt.xlabel('Number of Inlined Functions (0 = Standard Context)')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.ylim(0, 1.1)
    plt.legend(title='Models', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_impact_of_inlining.png'))
    plt.close()