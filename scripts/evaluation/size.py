import os
import seaborn as sns
import matplotlib.pyplot as plt

def genera(df, output_dir):
    categorie = ['1-10', '11-50', '51-100', '101-200', '200+']
    
    for tipo in df['Input_Type'].unique():
        df_filtrato = df[df['Input_Type'] == tipo]
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=df_filtrato, x='Size_Category', y='LLM Judge', hue='Model', palette='rocket_r', errorbar=None, order=categorie)
        
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3, fontsize=10, fontweight='bold', color='#333333')

        ax.set_xticks(range(len(categorie)))
        ax.set_xticklabels(categorie)

        for i, cat in enumerate(categorie):
            conteggio = len(df_filtrato[df_filtrato['Size_Category'] == cat]) // df_filtrato['Model'].nunique()
            ax.text(i, -0.07, f"({conteggio})", color='gray', fontsize=9, ha='center',va='top', transform=ax.get_xaxis_transform())
        
        plt.title(f"Performance by Function Size ({tipo} Context)", fontsize=16, fontweight='bold', pad=20)
        plt.ylim(0, 1.1)
        plt.ylabel('Average Score (0.0 - 1.0)')
        plt.xlabel('Function Size (LOC)', labelpad=25) 
        plt.legend(title='Models', bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'03_performance_by_size_{tipo.lower()}.png'))
        plt.close()