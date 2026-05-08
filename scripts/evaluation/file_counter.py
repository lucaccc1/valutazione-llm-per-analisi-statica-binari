import os
import json
from collections import defaultdict

root_dir = os.path.join("data", "evaluation_reports")
output_dir = os.path.join("data", "graphs")
output_filename = "counter_funzioni.txt"
filtro = "_qwen2.5-coder_14b_inlined_report.json" 

stats_funzioni = defaultdict(int)
stats_file = defaultdict(int)
totale_funzioni = 0
totale_file = 0

print(f"scanning: {root_dir}")

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if not filtro in file:
            continue
            
        percorso_relativo = os.path.relpath(root, root_dir)
        categoria = percorso_relativo.split(os.sep)[0] if percorso_relativo != "." else "root"
        stats_file[categoria] += 1
        totale_file += 1
        
        try:
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                lista_funzioni = json.load(f)
            
            if isinstance(lista_funzioni, list):
                num = len(lista_funzioni)
                stats_funzioni[categoria] += num
                totale_funzioni += num

        except Exception as e:
            print(f"error scanning {file}: {e}")

latex_table = [
    "\\begin{table}[h]",
    "    \\centering",
    "    \\small",
    "    \\begin{tabular}{lcc}",
    "        \\hline",
    "        \\textbf{Categoria (Dominio)} & \\textbf{Numero di File} & \\textbf{Numero di Funzioni} \\\\",
    "        \\hline"
]

for cat in sorted(stats_funzioni.keys()):
    latex_table.append(f"        {cat.capitalize()} & {stats_file[cat]} & {stats_funzioni[cat]} \\\\")

latex_table.extend([
    "        \\hline",
    f"        \\textbf{{Totale}} & \\textbf{{{totale_file}}} & \\textbf{{{totale_funzioni}}} \\\\",
    "        \\hline",
    "    \\end{tabular}",
    "    \\vspace{10pt}",
    "    \\caption{Distribuzione delle funzioni e dei file nel dataset suddivise per dominio di appartenenza.}",
    "    \\label{tab:distribuzione_domini}",
    "\\end{table}"
])

with open(os.path.join(output_dir, output_filename), "w", encoding="utf-8") as out:
    out.write("\n".join(latex_table))

print(f"latex table saved in: {output_filename}")