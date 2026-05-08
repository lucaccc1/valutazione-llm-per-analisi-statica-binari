compila il dataset (se hai aggiunto nuovi file c)
./scripts/build_dataset.sh

estrai i json con ida in background
./scripts/run_ida.sh

generazione dataset json completo
./scripts/build_dataset.sh && ./scripts/run_ida.sh && ./scripts/ida/inliner.py

avvia l'analisi dell'ia
python scripts/ai_engine/client.py

genera i grafici e le tabelle
python scripts/evaluation/main.py

scaricare nuovo modello
ollama pull modello

rimuovere modelli inutilizzati
ollama list
ollama rm modello

requirements
pip install ollama thefuzz scikit-learn google-genai python-dotenv pandas seaborn matplotlib Jinja2
