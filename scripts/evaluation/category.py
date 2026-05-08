import os
import seaborn as sns
import matplotlib.pyplot as plt

def genera(df, df_plot, output_dir):
    for tipo in df_plot['Input_Type'].unique():
        df_tipo = df_plot[df_plot['Input_Type'] == tipo]
        df_base_tipo = df[df['Input_Type'] == tipo]
        
        for cat in df_tipo['Category'].unique():
            df_cat = df_tipo[df_tipo['Category'] == cat]
            n_cat = len(df_base_tipo[df_base_tipo['Category'] == cat]) 
            nome_file_pulito = cat.replace('/', '_').replace('\\', '_')
            plt.figure(figsize=(12, 7))
            sns.barplot(data=df_cat, x='Metric', y='Score', hue='Model', palette='rocket', errorbar=None)
            plt.title(f"Category Analysis: {cat.upper()} ({tipo} Context)", fontsize=16, fontweight='bold', pad=20)
            plt.text(0.5, 1.02, f"Total functions analyzed: {n_cat}", transform=plt.gca().transAxes, ha='center', fontsize=12, color='gray')
            plt.ylim(0, 1.1) 
            plt.ylabel('Average Score (0.0 - 1.0)', fontsize=12)
            plt.legend(title='Models', bbox_to_anchor=(1.02, 1), loc='upper left')
            plt.tight_layout()
            nome_file = f'02_category_{nome_file_pulito}_{tipo.lower()}.png'
            plt.savefig(os.path.join(output_dir, nome_file))
            plt.close()