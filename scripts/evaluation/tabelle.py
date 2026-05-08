import os
import pandas as pd

def genera(df, df_funzioni, funzioni_controverse, modelli_presenti, metriche_colonne, output_dir):
    df['Category_Clean'] = df['Category'].str.capitalize()
    tabelle_output = []

    df['Inlining_Group'] = pd.cut(df['Inlined_Count'], bins=[-1, 0, 2, 5, 100], labels=['0 (Nodi Foglia)', '1-2 Funzioni', '3-5 Funzioni', '>5 Funzioni'])
    t4_df = df.pivot_table(index='Inlining_Group', columns='Model', values='LLM Judge', aggfunc='mean')
    t4 = t4_df.to_latex(float_format="%.3f", caption="Impatto Inlining sulle performance predittive.", label="tab:judge_inlining", na_rep="N/A")
    tabelle_output.append(("TABELLA 4: IMPATTO DELL'INLINING (GLOBALE)", t4))

    for tipo in df['Input_Type'].unique():
        df_tipo = df[df['Input_Type'] == tipo]
        
        if 'Input_Type' in df_funzioni.columns:
            df_funzioni_tipo = df_funzioni[df_funzioni['Input_Type'] == tipo]
            funzioni_controverse_tipo = funzioni_controverse[funzioni_controverse['Input_Type'] == tipo]
        else:
            df_funzioni_tipo = df_funzioni
            funzioni_controverse_tipo = funzioni_controverse

        colonne_escluse = ['GT_Name', 'Address', 'Size_Category', 'Input_Type', 'Average_Score', 'Variance']
        modelli_in_df = [c for c in df_funzioni_tipo.columns if c not in colonne_escluse]

        t1_df = df_tipo.groupby('Model')[metriche_colonne].mean().T
        t1 = t1_df.to_latex(float_format="%.3f", caption=f"Confronto globale metriche (Contesto: {tipo}).", label=f"tab:metriche_globali_{tipo.lower()}", escape=False)
        tabelle_output.append((f"TABELLA 1: CONFRONTO GLOBALE ({tipo.upper()})", t1))

        t2_df = df_tipo.pivot_table(index='Category_Clean', columns='Model', values=metriche_colonne, aggfunc='mean')
        t2_df = t2_df.reindex(columns=metriche_colonne, level=0)
        t2_df.index.name = 'Dominio / Categoria'
        t2 = t2_df.to_latex(float_format="%.3f", caption=f"Metriche di valutazione dettagliate per dominio applicativo (Contesto: {tipo}).", label=f"tab:metriche_dominio_{tipo.lower()}", na_rep="N/A", multicolumn=True)
        tabelle_output.append((f"TABELLA 2: METRICHE PER DOMINIO ({tipo.upper()})", t2))

        t3_df = df_tipo.pivot_table(index='Size_Category', columns='Model', values='LLM Judge', aggfunc='mean').reindex(['SMALL', 'MEDIUM', 'LARGE'])
        t3 = t3_df.to_latex(float_format="%.3f", caption=f"LLM Judge per dimensione (Contesto: {tipo}).", label=f"tab:judge_size_{tipo.lower()}", na_rep="N/A")
        tabelle_output.append((f"TABELLA 3: LLM JUDGE PER DIMENSIONE ({tipo.upper()})", t3))

        colonne_hard = ['GT_Name', 'Size_Category'] + modelli_in_df
        hard_failures = df_funzioni_tipo[df_funzioni_tipo['Average_Score'] == 0.0]
        if not hard_failures.empty:
            t5 = hard_failures[colonne_hard].head(10).to_latex(index=False, float_format="%.1f", caption=f"Top 10 Hard Failures (Contesto: {tipo}).", label=f"tab:hard_failures_{tipo.lower()}", escape=False)
            tabelle_output.append((f"TABELLA 5: TOP 10 HARD FAILURES ({tipo.upper()})", t5))

        t7_df = df_tipo.pivot_table(index='Size_Category', columns='Model', values='Execution_Time', aggfunc='mean').reindex(['SMALL', 'MEDIUM', 'LARGE'])
        t7 = t7_df.to_latex(float_format="%.2f", caption=f"Tempo di esecuzione in secondi (Contesto: {tipo}).", label=f"tab:execution_time_{tipo.lower()}", na_rep="N/A")
        tabelle_output.append((f"TABELLA 7: EFFICIENZA TEMPORALE ({tipo.upper()})", t7))

        if len(modelli_in_df) >= 2:
            agreement_matrix = pd.DataFrame(index=modelli_in_df, columns=modelli_in_df, dtype=float)
            for m1 in modelli_in_df:
                for m2 in modelli_in_df:
                    accordo = (df_funzioni_tipo[m1] == df_funzioni_tipo[m2]).mean() * 100
                    agreement_matrix.loc[m1, m2] = accordo
            
            t8 = agreement_matrix.to_latex(float_format="%.1f", caption=f"Matrice di accordo percentuale tra i modelli (Contesto: {tipo}).", label=f"tab:accordo_modelli_{tipo.lower()}", escape=False)
            tabelle_output.append((f"TABELLA 8: MATRICE DI ACCORDO ({tipo.upper()})", t8))

            df_controversy = df_funzioni_tipo[(df_funzioni_tipo['Average_Score'] > 0.0) & (df_funzioni_tipo['Average_Score'] < 1.0)]
            if not df_controversy.empty:
                win_rates = df_controversy[modelli_in_df].mean() * 100
                t9_df = pd.DataFrame(win_rates, columns=['Win Rate (%)'])
                t9_df.index.name = 'Model'
                t9 = t9_df.to_latex(float_format="%.1f", caption=f"Percentuale di successo sui casi controversi (Contesto: {tipo}).", label=f"tab:winrate_controversi_{tipo.lower()}", escape=False)
                tabelle_output.append((f"TABELLA 9: WIN RATE CONTROVERSI ({tipo.upper()})", t9))

    with open(os.path.join(output_dir, 'tabelle_latex_output.txt'), 'w', encoding='utf-8') as f:
        for titolo, text in tabelle_output:
            f.write(f"% {titolo}\n")
            f.write(f"% {'='*42}\n")
            f.write(f"{text}\n\n")