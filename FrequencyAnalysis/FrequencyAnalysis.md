Questo script implementa diverse operazioni di analisi del testo, tra cui il calcolo degli istogrammi di frequenza delle lettere, le distribuzioni empiriche di m-grammi e il calcolo dell'indice di coincidenza e dell'entropia per le distribuzioni di m-grammi.

## Funzionalità

- **Istogramma di Frequenza delle Lettere**: Calcola e traccia la frequenza di ciascuna lettera nel testo.
- **Distribuzione Empirica di M-grammi**: Calcola la distribuzione di m-grammi (sequenze di m caratteri) nel testo.
- **Indice di Coincidenza ed Entropia**: Calcola l'indice di coincidenza e l'entropia per la distribuzione empirica di m-grammi (internamente calcola la distribuzione empirica a seconda del paramatetro in input che indica la lunghezza degli m-grammi; questo significa che può essere eseguito in modo indipendente, non ci sono precedenze di command da rispettare)

## Prerequisiti

- **Python 3.x**
- **Librerie Richieste**:
    - argparse
    - json
    - math
    - collections
    - matplotlib
    - os
    - string

Installazione delle librerie richieste usando pip:

```shell
pip install library_name
```

## Utilizzo

Eseguire lo script dalla linea di comando con la modalità e gli argomenti desiderati.

### Argomenti da Linea di Comando

- `file`: Percorso del file di testo da analizzare.
- `--histogram`: Calcola e traccia l'istogramma di frequenza delle lettere.
- `--mgram`: Calcola la distribuzione empirica di m-grammi.
- `--coincidence-entropy`: Calcola l'indice di coincidenza e l'entropia della distribuzione empirica.

### Esempi

#### Calcolare e Tracciare l'Istogramma di Frequenza delle Lettere

```shell
python3 FrequencyAnalysis.py path/to/textfile.txt --histogram
```

#### Calcolare la Distribuzione Empirica di 3-grammi

```shell
python3 FrequencyAnalysis.py path/to/textfile.txt --mgram 3
```

#### Calcolare l'Indice di Coincidenza e l'Entropia per la Distribuzione di 3-grammi

```shell
python3 FrequencyAnalysis.py path/to/textfile.txt --coincidence-entropy 3
```

### Aiuto

Per informazioni dettagliate su utilizzo e opzioni, usare il flag `--help`:

```shell
python3 FrequencyAnalysis.py --help
```

### Note sull'implementazione

**Funzione `preprocess_text`**

**Descrizione:**

La funzione `preprocess_text` pre-elabora il testo rimuovendo la punteggiatura, gli spazi e convertendolo in minuscolo.

**Passaggi principali:**

1. **Rimozione della punteggiatura e degli spazi:**    
    - Utilizza `str.maketrans` e `str.translate` per rimuovere la punteggiatura.
    - Rimuove gli spazi e i caratteri di nuova linea.
2. **Conversione in minuscolo:**    
    - Converte tutto il testo in minuscolo per garantire coerenza nell'analisi.

**Funzione `index_of_coincidence_from_distribution`**

**Descrizione:**
L'indice di coincidenza si calcola nel seguente modo:   
  
$$  
IC = \frac{\sum_{i=1}^{n} f_i(f_i-1)}{n(n-1)}  
$$  
  
dove n è il numero totale di mgram e f il numero di occurrenze nel testo

L'indice di coincidenza si calcola nel seguente modo quando l'input è in inglese:   
  
$$  
IC \approx \sum_{i=1}^{n} q_i^2  
$$ 
dove q è la distribuzione empirica.

La funzione `index_of_coincidence_from_distribution` calcola l'indice di coincidenza della distribuzione di m-grammi usando la formula approssimativa dov' è presente q.

**Passaggi principali:**

1. **Calcolo dell'indice di coincidenza:**    
    - Somma i quadrati delle frequenze degli m-grammi 

**Funzione `entropy`**

**Descrizione:**

La funzione `entropy` calcola l'entropia della distribuzione di m-grammi.
L'entropia si calcola nel seguente modo:  
  
$$  
H(q) = -\sum_{a \in A} q_a \log_2 q_a  
$$

**Passaggi principali:**

1. **Calcolo dell'entropia:**    
    - Somma i prodotti delle frequenze degli m-grammi e dei loro logaritmi in base 2.

**Funzione `letter_frequency_histogram` **

**Descrizione:**

La `funzione letter_frequency_histogram` calcola e traccia l'istogramma di frequenza delle lettere.

Da wikipedia:  
  
```text  
  
A histogram is a visual representation of the distribution of quantitative data. To construct a histogram, the first step is to "bin" (or "bucket") the range of values— divide the entire range of values into a series of intervals—and then count how many values fall into each interval  
```  
  
Il range di valori che stiamo considerando per questo esercizio sono le lettere inglesi. Per ogni lettera dobbiamo calcolare le occorrenze nel testo in input. Sul diagramma, quindi, si avrà sull'asse x l'insieme delle lettere e sull'asse y la frequenza corrispondente.  
  
Prima di fare queste operazioni, bisogna pulire il testo in input. In particolare, è necessario eliminare la punteggiatura, gli spazi, il simbolo che indica una nuova riga nel testo, e trasformare tutto in lowercase.

**Passaggi principali:**

1. **Pre-elaborazione del testo:**    
    - Chiama `preprocess_text` per preparare il testo.
2. **Calcolo delle frequenze delle lettere:**    
    - Utilizza `collections.Counter` per contare le occorrenze delle lettere.
3. **Tracciamento dell'istogramma:**    
    - Utilizza `matplotlib` per creare un grafico a barre e salvarlo nel percorso di output specificato.

**Funzione `mgram_distribution_non_overlapping`**

**Descrizione:**

La funzione `mgram_distribution_non_overlapping` calcola la distribuzione empirica di m-grammi non sovrapposti.

**Passaggi principali:**

1. **Pre-elaborazione del testo:**    
    - Chiama `preprocess_text`  per preparare il testo.
2. **Calcolo delle frequenze degli m-grammi:**    
    - Divide il testo in m-grammi e utilizza `collections.Counter`  per contare le occorrenze.
3. **Calcolo della distribuzione:**    
    - Calcola la frequenza relativa di ciascun m-grammo.

## Esempio di Utilizzo

Per testare queste funzioni, è stato utilizzato il primo capitolo di "Moby Dick". Il testo del capitolo è contenuto nel file `1st_chap.txt` nella stessa cartella dello script. Nella cartella chiamata `output` si trovano i risultati ottenuti usando questo file come input per m=1,2,3,4.



