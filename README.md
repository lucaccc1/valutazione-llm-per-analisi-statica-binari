# RECoN/DIR

*Read this in other languages: [English](#english-version), [Italiano](#versione-italiana).*

## English Version

This repository contains the complete software infrastructure developed for the analysis, prediction, and semantic validation of decompiled C code using LLMs.

The project aims to evaluate the effectiveness of artificial intelligence models in understanding the logic of stripped binaries and reassigning meaningful names to functions and variables. The pipeline automates the entire workflow: it starts with source code compilation and structured extraction via IDA Pro, enriches the decompiled code context through inlining algorithms, and finally performs inference and automated evaluation. Model performances are measured using both classic algorithmic metrics and an advanced semantic metric based on the LLM-as-a-Judge paradigm.

This entire project is the subject of my bachelor's thesis at Sapienza University of Rome.

## Prerequisites

You need to have IDA and Ollama installed. Below are the official download links:

https://hex-rays.com/pricing?section=individuals

https://ollama.com/download

### Local Model Management (Ollama)

The system relies on Ollama to run inference models locally. Below are some useful commands for managing the models:

Download a new model:

    ollama pull <model_name>

List currently downloaded models:

    ollama list

Remove an unused model to free up disk space:

    ollama rm <model_name>

## Dependencies and Installation

Before running the scripts, you need to install the required Python libraries for API interaction, metrics calculation, and report generation:

    pip install ollama thefuzz scikit-learn google-genai python-dotenv pandas seaborn matplotlib Jinja2

## Main Workflow

Below are the commands to execute the different stages of the pipeline, from data preparation to the final evaluation.

### 1. Dataset Preparation

The repository includes the dataset used for the experiments detailed in the thesis, but it can be replaced with any dataset of C functions.

    ./scripts/build_dataset.sh

If new C source files have been added, you need to compile the updated binaries.

Extract structural information and decompiled code by running the script that connects to IDA Pro in the background:

    ./scripts/run_ida.sh

If desired, the JSON dataset can be analyzed with an expanded context using first-level semantic inlining:

    ./scripts/ida/inliner.py

**Complete Pipeline:**
To execute compilation, IDA extraction, and final JSON dataset generation in a single run:

    ./scripts/build_dataset.sh && ./scripts/run_ida.sh && ./scripts/ida/inliner.py

### 2. AI Inference

Start the analysis engine. The script will query the models locally (via Ollama) to generate predictions and use Gemini for semantic evaluation (LLM-as-a-Judge):

    python scripts/ai_engine/client.py

### 3. Report Generation

Process the results produced in the inference phase to automatically generate graphs and LaTeX-formatted tables for export:

    python scripts/evaluation/main.py

---

## Versione Italiana

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
