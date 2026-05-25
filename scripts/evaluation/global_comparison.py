import os
import seaborn as sns
import matplotlib.pyplot as plt

def genera(df, df_plot, output_dir):
    for tipo in df_plot['Input_Type'].unique():
        df_filtrato = df_plot[df_plot['Input_Type'] == tipo]
        n_funzioni = len(df[df['Input_Type'] == tipo])
        plt.figure(figsize=(12, 7))
        
        ax = sns.barplot(data=df_filtrato, x='Metric', y='Score', hue='Model', palette='rocket', errorbar=None)
        
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3, fontsize=10, fontweight='bold', color='#333333')

        plt.title(f"Global Performance Comparison ({tipo} Context)", fontsize=16, fontweight='bold', pad=20)
        plt.text(0.5, 1.02, f"Total functions analyzed: {n_funzioni}", transform=ax.transAxes, ha='center', fontsize=12, color='gray')
        plt.ylim(0, 1.1) 
        plt.ylabel('Average Score (0.0 - 1.0)', fontsize=12)
        plt.legend(title='Models', bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.tight_layout()
        nome_file = f'01_global_comparison_{tipo.lower()}.png'
        plt.savefig(os.path.join(output_dir, nome_file))
        plt.close()