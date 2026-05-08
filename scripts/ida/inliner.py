import json
import os
import glob
import re

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
input_dir = os.path.join(base_dir, 'data', 'llm_inputs')
output_dir = os.path.join(base_dir, 'data', 'llm_inputs_inlined')
json_files = glob.glob(os.path.join(input_dir, '**', '*.json'), recursive=True)
json_files = [f for f in json_files if not f.endswith('_report.json')]

if not json_files:
    print(f"no json files found in {input_dir}.")
    exit(0)

print("start recursive inlining...")

for input_file in json_files:
    percorso_relativo = os.path.relpath(input_file, input_dir)
    cartella_sottodominio = os.path.dirname(percorso_relativo)
    
    current_output_dir = os.path.join(output_dir, cartella_sottodominio)
    os.makedirs(current_output_dir, exist_ok=True)
    
    nome_file = os.path.basename(input_file)
    output_file = os.path.join(current_output_dir, nome_file.replace('.json', '_inlined.json'))
    
    print(f"processing: {percorso_relativo}")
    
    with open(input_file, 'r') as f:
        dati_input = json.load(f)

    dati_inlined = {}

    for indirizzo, dati in dati_input.items():
        codice_originale = dati.get('codice_decompilato', '')
        nuovo_record = dati.copy()
        indirizzi_chiamati = set(re.findall(r'\bsub_([0-9a-fA-F]+)\b', codice_originale))
        
        codice_da_aggiungere = ""
        funzioni_inlinate_effettive = 0
        
        for hex_addr in indirizzi_chiamati:
            chiave_chiamata = f"0x{hex_addr.lower()}"
            
            if chiave_chiamata.lower() == indirizzo.lower():
                continue
                
            if chiave_chiamata in dati_input:
                codice_chiamato = dati_input[chiave_chiamata].get('codice_decompilato', '')
                
                codice_da_aggiungere += f"// === START INLINED FUNCTION: sub_{hex_addr} ===\n"
                codice_da_aggiungere += codice_chiamato.strip() + "\n"
                codice_da_aggiungere += f"// === END INLINED FUNCTION: sub_{hex_addr} ===\n\n"
                funzioni_inlinate_effettive += 1

        if codice_da_aggiungere:
            codice_finale = (
                "// === MORE CONTEXT: CALLED FUNCTIONS ===\n" +
                codice_da_aggiungere +
                "// === MAIN FUNCTION TO ANALYZE ===\n" +
                codice_originale
            )
            nuovo_record['codice_decompilato'] = codice_finale
            nuovo_record['inlined_count'] = funzioni_inlinate_effettive
        else:
            nuovo_record['inlined_count'] = 0
            
        dati_inlined[indirizzo] = nuovo_record

    with open(output_file, 'w') as f:
        json.dump(dati_inlined, f, indent=4)

print("inlining successfully completed.")