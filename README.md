# RECoN/DIR

Questo repository contiene l'intera infrastruttura software sviluppata per l'analisi, la predizione e la validazione semantica di codice C decompilato attraverso l'utilizzo di LLM. 

Il progetto mira a valutare l'efficacia di modelli di intelligenza artificiale nel comprendere la logica di binari strippati e nel riassegnare nomi significativi a funzioni e variabili. La pipeline automatizza l'intero flusso di lavoro: parte dalla compilazione del codice sorgente e dall'estrazione strutturata tramite IDA Pro, arricchisce il contesto del codice decompilato attraverso algoritmi di inlining, ed esegue infine l'inferenza e la valutazione automatica. Le performance dei modelli sono misurate sia tramite metriche algoritmiche classiche, sia tramite una metrica semantica avanzata basata sul paradigma LLM-as-a-Judge.

L'intero progetto è oggetto della mia tesi di laurea triennale presso La Sapienza.

## Prerequisiti

Serve avere installato IDA e Ollama. Di seguito i link ufficiali per il download:

https://hex-rays.com/pricing?section=individuals

https://ollama.com/download

### Gestione Modelli Locali (Ollama)

Il sistema si appoggia a Ollama per l'esecuzione in locale dei modelli di inferenza. Di seguito i comandi utili per la gestione dei modelli:

Scaricare un nuovo modello:

    ollama pull <nome_modello>

Visualizzare la lista dei modelli attualmente scaricati:

    ollama list

Rimuovere un modello inutilizzato per liberare spazio su disco:

    ollama rm <nome_modello>

## Dipendenze e Installazione

Prima di eseguire gli script, è necessario installare le librerie Python richieste per l'interazione con le API, il calcolo delle metriche e la generazione dei report:

    pip install ollama thefuzz scikit-learn google-genai python-dotenv pandas seaborn matplotlib Jinja2

## Workflow Principale

Di seguito i comandi per eseguire le diverse fasi della pipeline, dalla preparazione dei dati alla valutazione finale.

### 1. Preparazione del Dataset

Nella repo è presente il dataset utilizzato per gli esperimenti necessari per la stesura della relazione, ma si può sostituire con qualsiasi dataset di funzioni C.

    ./scripts/build_dataset.sh

Se sono stati aggiunti nuovi file sorgente C, è necessario compilare i binari aggiornati.

Estrai le informazioni strutturali e il codice decompilato avviando lo script che si connette a IDA Pro in background:

    ./scripts/run_ida.sh

Se vuoi, si può analizzare il dataset JSON con un contesto espanso grazie ad un inlining semantico di primo livello:

    ./scripts/ida/inliner.py

**Pipeline Completa:**
Per eseguire in un'unica soluzione la compilazione, l'estrazione con IDA e la generazione del dataset JSON finale:

    ./scripts/build_dataset.sh && ./scripts/run_ida.sh && ./scripts/ida/inliner.py

### 2. Inferenza AI

Avvia il motore di analisi. Lo script interrogherà i modelli in locale (tramite Ollama) per generare le predizioni e utilizzera' Gemini per la valutazione semantica (LLM-as-a-Judge):

    python scripts/ai_engine/client.py

### 3. Generazione Report

Elabora i risultati prodotti nella fase di inferenza per generare automaticamente i grafici e le tabelle formattate in LaTeX per l'esportazione:

    python scripts/evaluation/main.py
