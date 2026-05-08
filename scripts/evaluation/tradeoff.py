import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def genera(df, output_dir):
    for tipo in df['Input_Type'].unique():
        df_filtrato = df[df['Input_Type'] == tipo].copy()
        df_filtrato['Result_Label'] = df_filtrato['LLM Judge'].map({0.0: 'Failed (0.0)', 1.0: 'Success (1.0)'})
        plt.figure(figsize=(10, 6))
        sns.violinplot(
            data=df_filtrato, 
            x='Result_Label', 
            y='Execution_Time', 
            hue='Model', 
            palette='rocket', 
            order=['Failed (0.0)', 'Success (1.0)'],
            density_norm='width',
            cut=0,
            inner="point" 
        )
        plt.title(f"Execution Time Profile: Success vs Failure ({tipo} Context)", fontsize=16, fontweight='bold', pad=20)
        plt.ylabel('Execution Time (Seconds)')
        plt.xlabel('Prediction Outcome')
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter())
        plt.grid(axis='y', which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.legend(title='Models', bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'08_tradeoff_time_vs_accuracy_{tipo.lower()}.png'), bbox_inches='tight')
        plt.close()