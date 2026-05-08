import os
import glob
import json
import pandas as pd

def carica_dati(base_dir):
    reports_dir = os.path.join(base_dir, 'data', 'evaluation_reports')
    modelli_attesi = ['qwen2.5-coder_14b', 'starcoder2_15b', 'deepseek-coder-v2_16b']
    dati_raccolti = []

    json_files = glob.glob(os.path.join(reports_dir, '**', '*.json'), recursive=True)
    if not json_files:
        raise FileNotFoundError("Nessun file JSON trovato.")

    for file_path in json_files:
        nome_file = os.path.basename(file_path)
        categoria = os.path.dirname(os.path.relpath(file_path, reports_dir)) or 'root'
            
        modello_usato = next((m for m in modelli_attesi if m in nome_file), "UNKNOWN")
        tipo_input = 'Inlined' if '_inlined_' in nome_file else 'Standard'
                
        try:
            with open(file_path, 'r') as f:
                funzioni_valutate = json.load(f)
                
            for record in funzioni_valutate:
                dim_info = record.get('dimension', {})
                record_base = {
                    'Category': categoria, 'Model': modello_usato, 'Input_Type': tipo_input,
                    'GT_Name': record.get('ground_truth_name', 'UNKNOWN'),
                    'Address': record.get('address', 'UNKNOWN'),
                    'Size_Category': dim_info.get('category', 'UNKNOWN'),
                    'LOC': dim_info.get('lines_of_code', 0),
                    'Inlined_Count': record.get('inlined_count', 0),
                    'Execution_Time': dim_info.get('execution_time', 0.0) 
                }

                if record.get('error_flag', False):
                    record_base.update({'Exact Match': 0.0, 'Levenshtein': 0.0, 'Jaccard': 0.0, 'Cosine': 0.0, 'LLM Judge': 0.0})
                else:
                    metrics = record.get('metrics', {})
                    record_base.update({
                        'Exact Match': metrics.get('exact_match', 0.0),
                        'Levenshtein': metrics.get('levenshtein_similarity', 0.0),
                        'Jaccard': metrics.get('jaccard_index', 0.0),
                        'Cosine': metrics.get('cosine_similarity', 0.0),
                        'LLM Judge': metrics.get('llm_as_a_judge', 0.0)
                    })
                dati_raccolti.append(record_base)
        except Exception as e:
            print(f"Errore lettura {nome_file}: {e}")

    df = pd.DataFrame(dati_raccolti)
    metriche_colonne = ['Exact Match', 'Levenshtein', 'Jaccard', 'Cosine', 'LLM Judge']
    df_plot = df.melt(id_vars=['Category', 'Model', 'Input_Type'], value_vars=metriche_colonne, var_name='Metric', value_name='Score')
    df['Inlined_Count'] = pd.to_numeric(df['Inlined_Count'], errors='coerce').fillna(0).astype(int)
    df_funzioni = df.pivot_table(index=['GT_Name', 'Address', 'Size_Category', 'Input_Type'], columns='Model', values='LLM Judge').reset_index().dropna()
    modelli_presenti = [m for m in modelli_attesi if m in df_funzioni.columns]
    df_funzioni['Average_Score'] = df_funzioni[modelli_presenti].mean(axis=1)
    df_funzioni['Variance'] = df_funzioni[modelli_presenti].var(axis=1)
    funzioni_controverse = df_funzioni.sort_values(by='Variance', ascending=False)

    return df, df_plot, df_funzioni, funzioni_controverse, modelli_presenti, metriche_colonne