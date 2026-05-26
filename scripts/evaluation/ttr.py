import os
import glob
import json
import re
import pandas as pd

def estrai_token(nome_funzione):
    if not nome_funzione or nome_funzione == "UNKNOWN":
        return []
    
    spaziato = re.sub(r'([a-z])([A-Z])', r'\1 \2', nome_funzione)
    spaziato = spaziato.replace('_', ' ').replace('.', ' ')
    return spaziato.lower().split()

current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(current_dir)
base_dir = os.path.dirname(scripts_dir)
gt_dir = os.path.join(base_dir, 'data', 'ground_truth')
output_dir = os.path.join(base_dir, 'data', 'graphs')
output_file = os.path.join(output_dir, 'tabella_ttr.txt')
os.makedirs(output_dir, exist_ok=True)

json_files = glob.glob(os.path.join(gt_dir, '**', '*.json'), recursive=True)

domini_stats = {}
for file_path in json_files:
    percorso_relativo = os.path.relpath(file_path, gt_dir)
    dominio = os.path.dirname(percorso_relativo) or "root"

    if dominio not in domini_stats:
        domini_stats[dominio] = {"num_funzioni": 0, "parole_totali": 0, "parole_uniche_set": set()}

    with open(file_path, 'r') as f:
        try:
            dati_gt = json.load(f)
            for address, info in dati_gt.items():
                tokens = estrai_token(info.get("nome_funzione_originale", ""))
                if tokens:
                    domini_stats[dominio]["num_funzioni"] += 1
                    domini_stats[dominio]["parole_totali"] += len(tokens)
                    domini_stats[dominio]["parole_uniche_set"].update(tokens)
        except Exception as e:
            print(f"Errore lettura {file_path}: {e}")

risultati_tabella = []
for dominio, stats in domini_stats.items():
    if stats["num_funzioni"] == 0 or stats["parole_totali"] == 0:
        continue
        
    parole_uniche = len(stats["parole_uniche_set"])
    
    risultati_tabella.append({
        "Dominio Applicativo": dominio.replace("_", " ").title(),
        "Funzioni Analizzate": stats["num_funzioni"],
        "Parole Totali": stats["parole_totali"],
        "Parole Uniche": parole_uniche,
        "TTR": parole_uniche / stats["parole_totali"]
    })

df = pd.DataFrame(risultati_tabella)
df = df.sort_values(by="TTR", ascending=True)

latex_table = df.to_latex(
    index=False,
    float_format="%.3f",
    caption="Analisi della dispersione lessicale (Type-Token Ratio) per dominio applicativo.",
    label="tab:word_dispersion",
    column_format="l c c c c"
)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(latex_table)
    
print(f"Tabella generata con successo usando Pandas! Salvata in: {output_file}")