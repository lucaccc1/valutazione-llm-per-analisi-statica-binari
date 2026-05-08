import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def genera(df, output_dir):
    plt.figure(figsize=(10, 6))
    ax = sns.lineplot(data=df, x='Inlined_Count', y='LLM Judge', hue='Model', palette='rocket_r', marker='o', errorbar=None, linewidth=2.5, markersize=8)
    inlined_vals = sorted(df['Inlined_Count'].unique())
    ax.set_xticks(inlined_vals)

    for val in inlined_vals:
        conteggio = len(df[df['Inlined_Count'] == val]) // df['Model'].nunique()
        ax.text(val, -0.07, f"({conteggio})", fontsize=9, color='gray', ha='center', va='top', transform=ax.get_xaxis_transform())

    plt.title("Impact of Inter-procedural Context on Accuracy", fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Average Accuracy (LLM Judge)')
    plt.xlabel('Number of Inlined Functions (0 = Standard Context)', labelpad=25)
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.ylim(0, 1.1)
    plt.legend(title='Models', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_impact_of_inlining.png'))
    plt.close()