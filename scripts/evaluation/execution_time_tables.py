import os
import glob
import json
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(current_dir)
base_dir = os.path.dirname(scripts_dir)
reports_dir = os.path.join(base_dir, 'data', 'evaluation_reports')
output_dir = os.path.join(base_dir, 'data', 'graphs')
os.makedirs(output_dir, exist_ok=True)

output_file_summary = os.path.join(output_dir, 'tabella_tempi_output.txt')
output_file_top10 = os.path.join(output_dir, 'tabella_top10_lente.txt')

json_files = glob.glob(os.path.join(reports_dir, '**', '*.json'), recursive=True)
if not json_files:
    print("Nessun report trovato in:", reports_dir)
    exit()

dati = []

for file_path in json_files:
    is_inlined = "inlined" in file_path.lower()
    contesto = "Inlined" if is_inlined else "Standard"

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            records = json.load(f)
            for rec in records:
                t_exec = rec.get("dimension", {}).get("execution_time", 0.0)
                loc = rec.get("dimension", {}).get("lines_of_code", 0)
                score = rec.get("metrics", {}).get("llm_as_a_judge", 0.0)
                error_flag = rec.get("error_flag", False)
                pred_name = rec.get("ai_predicted_name", "UNKNOWN")

                if error_flag:
                    status = "Errore di Formato"
                    out_len = 0
                elif score == 1.0:
                    status = "Successo"
                    out_len = len(str(pred_name)) if pred_name and pred_name != "UNKNOWN" else 0
                else:
                    status = "Fallimento"
                    out_len = len(str(pred_name)) if pred_name and pred_name != "UNKNOWN" else 0

                if t_exec and t_exec > 0:
                    dati.append({
                        "Contesto": contesto,
                        "Risposta_AI": pred_name,
                        "Risultato Predizione": status,
                        "Tempo Medio (s)": t_exec,
                        "LOC": loc,
                        "Output_Medio": out_len,
                        "Judge_Score": score
                    })
        except Exception as e:
            pass

df = pd.DataFrame(dati)
if df.empty:
    print("Nessun dato valido estratto.")
    exit()

agg_df = df.groupby(["Contesto", "Risultato Predizione"]).agg(
    Campioni=("Risultato Predizione", "count"),
    Tempo_Medio=("Tempo Medio (s)", "mean"),
    LOC_Medie=("LOC", "mean"),
    Output_Medio=("Output_Medio", "mean")
).reset_index()

ordine = {"Successo": 1, "Fallimento": 2, "Errore di Formato": 3}
agg_df["Order"] = agg_df["Risultato Predizione"].map(ordine)
agg_df = agg_df.sort_values(["Contesto", "Order"]).drop(columns=["Order"])

agg_df["Lunghezza Output (char)"] = agg_df["Output_Medio"].map(lambda x: f"{x:.1f}")
agg_df = agg_df.rename(columns={"Tempo_Medio": "Tempo Medio (s)", "LOC_Medie": "LOC Medie"}).drop(columns=["Output_Medio"])

latex_summary = agg_df.to_latex(
    index=False, float_format="%.2f",
    caption="Relazione quantitativa tra l'esito della predizione, la dimensione dell'input e la lunghezza dell'output generato.",
    label="tab:tempi_lunghezza_output", column_format="l l c c c c"
)
latex_summary = latex_summary.replace("\\begin{tabular}", "\\resizebox{\\textwidth}{!}{%\n\\begin{tabular}").replace("\\end{tabular}", "\\end{tabular}%\n}")

with open(output_file_summary, 'w', encoding='utf-8') as f:
    f.write(latex_summary)

print(f"Tabella generata con successo. Salvata in: {output_file_summary}")

top10_df = df.sort_values(by="Tempo Medio (s)", ascending=False).head(10)
top10_latex_df = top10_df[["Contesto", "LOC", "Tempo Medio (s)", "Risposta_AI", "Judge_Score"]].copy()

top10_latex_df = top10_latex_df.rename(columns={
    "Tempo Medio (s)": "Tempo (s)",
    "Risposta_AI": "Predizione AI",
    "Judge_Score": "Score"
})

top10_latex_df["Predizione AI"] = top10_latex_df["Predizione AI"].apply(lambda x: f"\\texttt{{{str(x).replace('_', '\\_')}}}")

latex_top10 = top10_latex_df.to_latex(
    index=False, float_format="%.2f",
    caption="Analisi dei casi peggiori: dettaglio strutturale e testuale delle 10 computazioni più lente.",
    label="tab:top10_slowest", column_format="l c c l c"
)
latex_top10 = latex_top10.replace("\\begin{tabular}", "\\resizebox{\\textwidth}{!}{%\n\\begin{tabular}").replace("\\end{tabular}", "\\end{tabular}%\n}")

with open(output_file_top10, 'w', encoding='utf-8') as f:
    f.write(latex_top10)

print(f"Tabella generata con successo. Salvata in: {output_file_top10}")