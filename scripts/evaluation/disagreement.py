import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def genera(df_funzioni, output_dir):
    categorie = ['1-10', '11-50', '51-100', '101-200', '200+']
    
    for tipo in df_funzioni['Input_Type'].unique():
        df_filtrato = df_funzioni[df_funzioni['Input_Type'] == tipo]
        
        if 'Variance' not in df_filtrato.columns or df_filtrato['Variance'].isna().all():
            continue

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=df_filtrato, x='Size_Category', y='Variance', hue='Size_Category', palette='rocket_r', order=categorie, legend=False)
        ax.set_xticks(range(len(categorie)))
        ax.set_xticklabels(categorie)

        for i, cat in enumerate(categorie):
            conteggio = len(df_filtrato[df_filtrato['Size_Category'] == cat])
            ax.text(i, -0.07, f"({conteggio})", color='gray', fontsize=9, ha='center', va='top', transform=ax.get_xaxis_transform())

        plt.title(f"Average Model Disagreement by Function Size ({tipo} Context)", fontsize=16, fontweight='bold', pad=20)
        plt.ylabel("Disagreement Frequency") 
        plt.xlabel("Function Size (LOC)", labelpad=25)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0)) 
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'05_variance_bar_size_{tipo.lower()}.png'))
        plt.close()