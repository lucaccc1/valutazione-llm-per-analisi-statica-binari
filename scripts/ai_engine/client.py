import json
import ollama
import os
import sys
import glob
from thefuzz import fuzz
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
from google.genai import types
import os
import time
from dotenv import load_dotenv 

load_dotenv() 
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

def dimensione(codice):
    loc = len(codice.strip().split('\n'))

    if loc <= 10:
        dim = 'SMALL'
    elif loc <= 50:
        dim = 'MEDIUM'
    else:
        dim = 'LARGE'

    return dim, loc

def levenshtein_evaluation(gt, ai):
    if not gt or not ai or gt == "UNKNOWN":
        return 0.0
    
    gt = gt.strip().lower()
    ai = ai.strip().lower()
    ratio_crudo = fuzz.ratio(gt, ai) / 100

    gt_lavorata = gt.replace("_", " ")
    ai_lavorata = ai.replace("_", " ")
    ratio_lavorato = fuzz.ratio(gt_lavorata, ai_lavorata) / 100

    return max(ratio_crudo, ratio_lavorato)

def estrai_parole_chiave(nome_funzione):
    spaziato = re.sub(r'([a-z])([A-Z])', r'\1 \2', nome_funzione)
    spaziato = spaziato.replace('_', ' ').replace('.', ' ')
    return set(spaziato.lower().split())

def jaccard_coverage_evaluation(gt, ai):
    if not gt or not ai or gt == "UNKNOWN":
        return 0.0

    set_gt = estrai_parole_chiave(gt)
    set_ai = estrai_parole_chiave(ai)

    if len(set_gt) == 0:
        return 0.0
        
    intersezione = len(set_gt.intersection(set_ai))
    
    return round(intersezione / len(set_gt), 2)

def cosine_evaluation(gt, ai):
    if not gt or not ai or gt == "UNKNOWN":
        return 0.0

    gt = gt.replace("_", " ").strip().lower()
    ai = ai.replace("_", " ").strip().lower()

    if len(gt) == 0 or len(ai) == 0:
        return 0.0

    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 3))
    
    try:
        tfidf_matrix = vectorizer.fit_transform([gt, ai])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score), 2)
    except ValueError:
        return 0.0
    
def llm_judge(codice_gt, ai_name, tentativi = 3):
    if not codice_gt or not ai_name or ai_name == "UNKNOWN":
        return 0.0
    
    prompt_giudice = f"""
    you're an experienced C programmer and reverse engineer.
    your task is to evaluate if a proposed function name accurately describes the behavior of the provided C code.

    C code:
    ```c
    {codice_gt}
    ```
    proposed function name: "{ai_name}"

    does the proposed name semantically fit the logic, operations, and purpose of the code?
    answer ONLY with the number 1 if it is a good semantic fit, or 0 if it is not.
    do not be too harsh: if it captures the main logic, accept it.
    do not add any additional text, explanation, or punctuation.
    """

    for tentativo in range(tentativi):
        try:
            response = client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=prompt_giudice,
                config=types.GenerateContentConfig(
                    temperature=0.0
                )
            )
            
            voto = response.text.strip()
            if "1" in voto:
                return 1.0
            else:
                return 0.0
            
        except Exception as e:
            errore_str = str(e) 
            print(f"        gemini api error (tentativo {tentativo+1}): {errore_str}")
            
            if "503" in errore_str or "429" in errore_str:
                attesa = 5 * (tentativo + 1)
                time.sleep(attesa)
                continue  
            else:
                return 0.0
            
    return 0.0

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# input_dir = os.path.join(base_dir, 'data', 'llm_inputs')
input_dir = os.path.join(base_dir, 'data', 'llm_inputs_inlined')
gt_dir = os.path.join(base_dir, 'data', 'ground_truth')
output_dir = os.path.join(base_dir, 'data', 'evaluation_reports')

modello = 'qwen2.5-coder:14b'
# modello = 'deepseek-coder-v2:16b'
# modello = 'starcoder2:15b'
modello_safe = modello.replace(":", "_")

if not os.path.exists(input_dir):
    print(f"error: input directory not found at {input_dir}")
    sys.exit(1)

if not os.path.exists(gt_dir):
    print(f"error: ground truth directory not found at {gt_dir}")
    sys.exit(1)

os.makedirs(output_dir, exist_ok=True)

json_files = glob.glob(os.path.join(input_dir, '**', '*.json'), recursive=True)

if not json_files:
    print(f"error: no json files found in {input_dir}")
    sys.exit(0)

print(f"starting analysis and evaluation setup with {modello}...")

totale_file = len(json_files)

for index_file, input_file in enumerate(json_files, 1):
    percorso_relativo = os.path.relpath(input_file, input_dir)
    sub_dir = os.path.dirname(percorso_relativo)
    nome_file_originale = os.path.basename(input_file)
    is_inlined = "inlined" in input_dir
    suffix = "_inlined.json" if is_inlined else ".json"
    tag = "inlined" if is_inlined else "standard"
    nome_base = nome_file_originale.replace(suffix, "").replace("_stripped", "")
    nome_file_output = f"{nome_base}_{modello_safe}_{tag}_report.json"
    nome_per_gt = f"{nome_base}_debug.json" 
    
    current_output_dir = os.path.join(output_dir, sub_dir)
    os.makedirs(current_output_dir, exist_ok=True)
    
    output_file = os.path.join(current_output_dir, nome_file_output)
    gt_file = os.path.join(gt_dir, sub_dir, nome_per_gt)

    if not os.path.exists(gt_file):
        print(f"error: skipping {percorso_relativo}, ground truth file missing at {gt_file}")
        continue

    with open(input_file, 'r') as f:
        dati_input = json.load(f)
        
    with open(gt_file, 'r') as f:
        dati_gt = json.load(f)

    risultati_valutazione = []
    file_errors = False

    print(f"[{index_file}/{totale_file}] - processing file: {nome_file_originale}...")

    totale_funzioni = len(dati_input)

    for index_func, (indirizzo, dati) in enumerate(dati_input.items(), 1):
        codice = dati['codice_decompilato']
        nome_corrente = dati['nome_corrente']
        inlined_count = dati.get('inlined_count', 0)
        dict_variabili = dati.get('variabili', {})
        lista_nomi_variabili = ", ".join(dict_variabili.keys())
        info_gt = dati_gt.get(indirizzo, {})
        nome_originale_gt = info_gt.get('nome_funzione_originale', 'UNKNOWN')
        codice_gt = info_gt.get('codice_decompilato', codice)

        if indirizzo not in dati_gt:
            print(f"    skipping function {nome_corrente}: filtered out from ground truth.")
            continue

        print(f"    [{index_func}/{totale_funzioni}] - processing function: {nome_originale_gt}...")

        prompt = f"""
        you are an expert reverse engineer and C programmer analyzing decompiled binary code.

        ## context
        you are given a decompiled C function named `{nome_corrente}` with hidden variable names: {lista_nomi_variabili}.
        the code was produced by a decompiler (IDA Pro), so it may contain artifacts like unnecessary casts, split variables, or non-idiomatic patterns.

        ## your task
        carefully read the decompiled code below and reason step by step about:
        - what system calls or library functions are invoked, and what they imply
        - how data flows between variables (reads, writes, transformations)
        - the overall control flow (loops, conditions, early exits)
        - any domain clues (networking, file I/O, crypto, string processing, etc.)

        then produce:
        1. **a descriptive snake_case name for the function** that captures its primary responsibility.
        - special rule: if the function handles `argc`/`argv`, orchestrates program startup, and returns an exit code → name it exactly `main`.
        - prefer verb-noun names: `send_message`, `parse_header`, `connect_to_server`.
        2. **a descriptive snake_case name for each variable** based on its role in the code.
        - prefer names like `socket_fd`, `bytes_read`, `input_buffer` over generic ones like `var1`.
        - decompiler artifacts (e.g. split `__int128` chunks used as padding) can be named `padding_N`.

        ## output format
        reply with **only** a valid JSON object — no explanation, no markdown, no extra text:
        {{
            "suggested_function_name": "chosen_name",
            "suggested_variables": {{
                "fictitious_name_1": "suggested_name_1",
                "fictitious_name_2": "suggested_name_2"
            }}
        }}

        ## code to Analyze
        ```c
        {codice}
        ```
        """

        size, loc = dimensione(codice)

        record_valutazione = {
            "address": indirizzo,
            "ida_stripped_name": nome_corrente,
            "ground_truth_name": nome_originale_gt,          
            "ai_predicted_name": None,
            "dimension": {
                "category": size,
                "lines_of_code": loc,
                "execution_time": None
            },
            "metrics": {
                "exact_match": None,
                "levenshtein_similarity": None,
                "jaccard_index": None,
                "cosine_similarity": None,
                "llm_as_a_judge": None
            },
            "error_flag": False,
            "inlined_count": inlined_count
        }

        try:
            t_start = time.time()

            risposta = ollama.chat(model=modello, messages=[
                {'role': 'user', 'content': prompt}
            ], format='json')

            t_end = time.time()
            tempo_totale = round(t_end - t_start, 2)
            
            contenuto_risposta = risposta['message']['content'].strip()
            
            if contenuto_risposta.startswith("```"):
                contenuto_risposta = contenuto_risposta.strip("`").replace("json", "", 1).strip()

            try:
                dati_ia = json.loads(contenuto_risposta)
                nome_predetto = dati_ia.get("suggested_function_name")
                record_valutazione["ai_predicted_name"] = nome_predetto

                if nome_predetto == nome_originale_gt:
                    exact_match = 1
                else:
                    exact_match = 0

                record_valutazione["metrics"]["exact_match"] = exact_match
                record_valutazione["metrics"]["levenshtein_similarity"] = levenshtein_evaluation(nome_originale_gt, nome_predetto)
                record_valutazione["metrics"]["jaccard_index"] = jaccard_coverage_evaluation(nome_originale_gt, nome_predetto)
                record_valutazione["metrics"]["cosine_similarity"] = cosine_evaluation(nome_originale_gt, nome_predetto)
                record_valutazione["metrics"]["llm_as_a_judge"] = llm_judge(codice_gt, nome_predetto)
                record_valutazione["dimension"]["execution_time"] = tempo_totale

                time.sleep(4)

            except json.JSONDecodeError:
                print(f"error: invalid json from ai for {nome_corrente} in {nome_file_originale}")
                file_errors = True
                record_valutazione["error_flag"] = True

        except Exception as e:
            print(f"error: communication error for {nome_corrente} in {nome_file_originale}: {e}")
            file_errors = True
            record_valutazione["error_flag"] = True

        risultati_valutazione.append(record_valutazione)

    with open(output_file, 'w') as f:
        json.dump(risultati_valutazione, f, indent=4)

    if file_errors:
        print(f"file processed with errors: {nome_file_originale}")
    else:
        print(f"file processed successfully: {nome_file_originale}")

print("analysis setup completed for all files.")
