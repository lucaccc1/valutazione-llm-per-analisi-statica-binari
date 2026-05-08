import os
import seaborn as sns
import matplotlib.pyplot as plt

import category
import data_loader
import execution_size
import global_comparison
import inlining
import agreement_matrix_controversial_functions
import size
import tabelle
import tradeoff
import disagreement

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
output_grafici_dir = os.path.join(base_dir, 'data', 'graphs')
os.makedirs(output_grafici_dir, exist_ok=True)

sns.set_theme(style="darkgrid")
plt.rcParams['figure.dpi'] = 300

print("loading data...")
df, df_plot, df_funzioni, funzioni_controverse, modelli_presenti, metriche_colonne = data_loader.carica_dati(base_dir)

print("generating graphs...")
global_comparison.genera(df, df_plot, output_grafici_dir)
category.genera(df, df_plot, output_grafici_dir)
execution_size.genera(df, output_grafici_dir)
inlining.genera(df, output_grafici_dir)
size.genera(df, output_grafici_dir)
disagreement.genera(df_funzioni, output_grafici_dir)
agreement_matrix_controversial_functions.genera(df_funzioni, output_grafici_dir)
tradeoff.genera(df, output_grafici_dir)

print("generating latex tables...")
tabelle.genera(df, df_funzioni, funzioni_controverse, modelli_presenti, metriche_colonne, output_grafici_dir)

print("analysis completed successfully!")