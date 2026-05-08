import os
import seaborn as sns
import matplotlib.pyplot as plt

def genera(df, output_dir):
    for tipo in df['Input_Type'].unique():
        df_filtrato = df[df['Input_Type'] == tipo]
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_filtrato, x='Size_Category', y='Execution_Time', hue='Model', palette='rocket', errorbar=None, order=['SMALL', 'MEDIUM', 'LARGE'])
        plt.title(f"Execution Time by Function Size ({tipo} Context)", fontsize=16, fontweight='bold', pad=20)
        plt.ylabel('Average Time (Seconds)')
        plt.xlabel('Function Size')
        plt.legend(title='Models', bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'07_execution_time_by_size_{tipo.lower()}.png'))
        plt.close()