# Sviluppo di un modello per la simulazione della rete Twitter

### Un approccio basato sull'omofilia

Autori: **Comi Marco** & **Gravina Marco**

GitHub: **@kin0992** & **@mgravina1**

### Dipendenze:
1. NumPy
2. Scipy
3. matplotlib
4. networkx

### Main file: 
+ **twitter-simulation.py**: contiene la logica del simulatore

+ **variabili.py**: file di configurazione delle variabili

### Organizzazione files

Il file .py contenente la logica del simulatore deve stare nella stessa cartella del file **pycxsimulator.py**.

La cartella **data** contiene delle sottocartelle in cui vengono salvati alcuni file utili durante la fase di analisi.

Le sotto cartelle sono:

+ **csv**: cartella destinazione dei .csv generati dai file .json

+ **gephi**: cartella destinazione dei file .gexf usati per visualizzare la rete simulata

+ **grafici**: cartella destinazione dei file .csv utilizzati per analizzare i dati di ogni singolo nodo

+ **json**: cartella destinazione dei file .json

+ **nodi_da_controllare**: cartella destinazione dei file .txt in cui vengono salvati i nodi che effettuani i tweet fortunati e i retweet dei vip ai nodi non vip

### File di supporto:
+ **clear_file.py**: script per rimuovere i file nelle cartelle prima di iniziare una nuova simulazione

+ **json_to_csv.py**: script che converte i dati dal formato json al formato csv

+ **csv_script.py**: script che da tutti i file .csv, prende solo le righe relative ad un nodo selezionato e crea un file .csv nuovo
