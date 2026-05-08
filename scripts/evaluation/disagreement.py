import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def genera(df_funzioni, output_dir):
    for tipo in df_funzioni['Input_Type'].unique():
        df_filtrato = df_funzioni[df_funzioni['Input_Type'] == tipo]
        
        if 'Variance' not in df_filtrato.columns or df_filtrato['Variance'].isna().all():
            continue

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=df_filtrato, x='Size_Category', y='Variance', hue='Size_Category', palette='rocket_r', order=['SMALL', 'MEDIUM', 'LARGE'], legend=False)
        plt.title(f"Average Model Disagreement by Function Size ({tipo} Context)", fontsize=16, fontweight='bold', pad=20)
        plt.ylabel("Disagreement Frequency") 
        plt.xlabel("Function Size")
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0)) 
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'05_variance_bar_size_{tipo.lower()}.png'))
        plt.close()