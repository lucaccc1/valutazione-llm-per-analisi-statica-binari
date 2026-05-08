import os
import seaborn as sns
import matplotlib.pyplot as plt

def genera(df, output_dir):
    for tipo in df['Input_Type'].unique():
        df_filtrato = df[df['Input_Type'] == tipo]
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_filtrato, x='Size_Category', y='LLM Judge', hue='Model', palette='rocket', errorbar=None, order=['SMALL', 'MEDIUM', 'LARGE'])
        plt.title(f"Performance by Function Size ({tipo} Context)", fontsize=16, fontweight='bold', pad=20)
        plt.ylim(0, 1.1)
        plt.ylabel('Average Score (0.0 - 1.0)')
        plt.legend(title='Models', bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'03_performance_by_size_{tipo.lower()}.png'))
        plt.close()