import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def genera(df_funzioni, output_dir):
    for tipo in df_funzioni['Input_Type'].unique():
        df_filtrato = df_funzioni[df_funzioni['Input_Type'] == tipo].copy()
        colonne_escluse = ['GT_Name', 'Address', 'Size_Category', 'Input_Type', 'Average_Score', 'Variance']
        modelli = [c for c in df_filtrato.columns if c not in colonne_escluse]
        
        if len(modelli) < 2:
            print(f" -> Saltato grafico 06_differenze_modelli ({tipo}): Servono almeno 2 modelli per confrontarli.")
            continue

        agreement_matrix = pd.DataFrame(index=modelli, columns=modelli, dtype=float)
        for m1 in modelli:
            for m2 in modelli:
                accordo = (df_filtrato[m1] == df_filtrato[m2]).mean() * 100
                agreement_matrix.loc[m1, m2] = accordo

        plt.figure(figsize=(8, 6))
        sns.heatmap(agreement_matrix, annot=True, fmt=".1f", cmap="rocket_r", vmin=0, vmax=100, cbar_kws={'label': 'Agreement %'})
        plt.title(f"Model Pairwise Agreement % ({tipo} Context)", fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'06a_model_agreement_heatmap_{tipo.lower()}.png'))
        plt.close()

        df_controversy = df_filtrato[(df_filtrato['Average_Score'] > 0.0) & (df_filtrato['Average_Score'] < 1.0)]
        
        if not df_controversy.empty:
            win_rates = df_controversy[modelli].mean() * 100
            df_plot = win_rates.reset_index()
            df_plot.columns = ['Model', 'Win Rate (%)']
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(data=df_plot, x='Model', y='Win Rate (%)', hue='Model', palette='magma', legend=False)

            plt.title(f"Performance on Controversial Functions ({tipo} Context)\n(Subset of {len(df_controversy)} functions where models disagreed)", fontsize=14, fontweight='bold', pad=20)
            plt.ylabel("Accuracy (%) on Controversial Set")
            plt.xlabel("Models")
            plt.ylim(0, 105)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f'06b_controversial_winrate_{tipo.lower()}.png'))
            plt.close()