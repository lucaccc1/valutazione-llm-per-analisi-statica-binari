import os
import json

root_dir = os.path.join("data", "evaluation_reports")

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if not file.endswith('.json'):
            continue
            
        percorso = os.path.join(root, file)
        
        try:
            with open(percorso, 'r', encoding='utf-8') as f:
                dati = json.load(f)
            
            if not isinstance(dati, list):
                continue

            modificato = False
            
            for func in dati:
                if "dimension" in func and "lines_of_code" in func["dimension"]:
                    loc = func["dimension"]["lines_of_code"]
                    
                    if loc <= 10:
                        nuova_cat = "1-10"
                    elif loc <= 50:
                        nuova_cat = "11-50"
                    elif loc <= 100:
                        nuova_cat = "51-100"
                    elif loc <= 200:
                        nuova_cat = "101-200"
                    else:
                        nuova_cat = "200+"
                        
                    if func["dimension"].get("category") != nuova_cat:
                        func["dimension"]["category"] = nuova_cat
                        modificato = True
            
            if modificato:
                with open(percorso, 'w', encoding='utf-8') as f:
                    json.dump(dati, f, indent=4, ensure_ascii=False)
                    
        except Exception:
            pass

print("update completed!")