Questo script implementa la encryption e decryption del cifrario di Hill, oltre al known plaintext attack.
## Funzionalità

- **Encryption**: Cifra messaggi in chiaro utilizzando una chiave K
$$
C = P * K \mod 26
$$
- **Decryption**: Decifra messaggi cifrati utilizzando l'inversa della chiave K.
$$
P = C * K^{-1} \mod 26
$$
- **Known plaintext attack**: Recupera la matrice K quando vengono forniti sia il testo in chiaro (P) sia il testo cifrato corrispondente (C).
$$
K = C * P^{-1} \mod 26
$$

## Prerequisiti

- **Python 3.x**
- **Librerie Richieste**:
    - sympy
    - numpy

Installazione delle librerie richieste usando pip:

```shell
pip install numpy
```

```shell
pip install sympy
```

## Utilizzo

Eseguire lo script dalla linea di comando con la modalità e gli argomenti desiderati.

### Argomenti da Linea di Comando

- `--mode`: Modalità di operazione. Le scelte sono `encrypt`, `decrypt` o `known-plaintext-attack`. Il valore predefinito è `encrypt`.
- `--message`: Il messaggio da usare nella modalità `encrypt` o `decrypt`.
- `--key`: La matrice K come stringa, ad esempio `'7,4;11,11'` per una matrice `2x2`.
- `--plaintext`: Testo in chiaro per il `known-plaintext-attack`.
- `--ciphertext`: Testo cifrato per il `known-plaintext-attack`. 
- `--key-length`: La dimensione della matrice K (usata per il `known-plaintext-attack`.).

### Esempi

#### Encryption

```shell
python3 HillCipher.py --mode encrypt --message "IL TUO MESSAGGIO QUI" --key "7,4;11,11"
```

#### Decryption

```shell
python3 HillCipher.py --mode decrypt --message "MESSAGGIO CIFRATO QUI" --key "7,4;11,11"
```

#### Known plaintext attack

```shell
python3 HillCipher.py --mode known-plaintext-attack --plaintext "IL TUO TESTO IN CHIARO QUI" --ciphertext "TESTO CIFRATO CORRISPONDENTE QUI" --key-length 2
```

### Aiuto

Per informazioni dettagliate su utilizzo e opzioni, usare il flag `--help`:

```shell
python3 HillCipher.py --help
```


### Note sull'implementazione
**Funzione encrypt**

**Descrizione:**

La funzione **encrypt** cifra un messaggio di testo in chiaro utilizzando una matrice chiave e il modulo 26 (numero di lettere nell'alfabeto inglese).

**Passaggi principali:**

1. **Preprocessing del messaggio:**    
    - Chiama ***preprocess_input(message)*** per convertire il messaggio in minuscolo, rimuovere spazi e punteggiatura. In questo modo si garantisce che il messaggio sia in un formato standard per la cifratura, evitando problemi con caratteri non alfabetici.
2. **Conversione in numeri:**
    - Utilizza ***convert_to_numbers(message)*** per convertire ogni lettera in un numero tra 0 e 25 (`a=0`, `b=1`, ..., `z=25`) per facilitare le operazioni matematiche necessarie per la cifratura.
3. **Divisione in blocchi:**    
	- Il cifrario di Hill richiede che il testo sia suddiviso in array di dimensione compatibile con la matrice chiave.
    - Chiama ***get_blocks(numbers, key_length)*** per suddividere i numeri in una matrice che ha come numero di righe la lunghezza della chiave. Se necessario, aggiunge lettere di padding (`'z'`, ovvero `25`) per completare l'ultimo blocco.
5. **Cifratura del messaggio:**    
    - Viene eseguito il prodotto tra la matrice chiave e i blocchi generati a partire dal messaggio, applicando poi il modulo 26.
5. **Conversione in testo cifrato:**    
    - Converte i numeri risultanti dai blocchi cifrati nuovamente in lettere.
    - Unisce tutti i blocchi per ottenere il testo cifrato finale.

**Funzioni di libreria utilizzate:**

- ***numpy.dot()***: Calcola il prodotto tra la matrice chiave e i blocchi di testo.
- ***numpy.reshape()*** e ***numpy.transpose():*** Gestiscono la forma e l'orientamento dei blocchi di dati. L'uso di NumPy ottimizza le operazioni matriciali e rende il codice più efficiente.

---

**Funzione decrypt**

**Descrizione:**

La funzione **decrypt** decifra un testo cifrato utilizzando l'inversa della matrice chiave.

**Passaggi principali:**

1. **Preprocessing del messaggio:**    
    - Simile alla cifratura, prepara il testo cifrato per l'elaborazione.
2. **Calcolo dell'inversa della chiave:**    
    - Chiama ***get_inverse(key, N)*** per ottenere l'inverso modulare della matrice chiave (mod 26).
    - Utilizza la funzione ***inv_mod()*** dalla libreria ***sympy*** per calcolare l'inversa.
3. **Decifratura:**    
    - Riutilizza la funzione ***encrypt*** passando come chiave l'inversa appena calcolata. Poiché la decifratura è matematicamente simile alla cifratura (usando l'inversa della chiave), si evita la duplicazione del codice.

**Funzioni di libreria utilizzate:**

- ***sympy.Matrix.inv_mod():*** Calcola l'inversa modulare di una matrice.
- ***numpy.linalg.det():*** Calcola il determinante della matrice
- ***numpy.gcd()***: Determina se il determinante e il modulo sono coprimi.

Note:
- **Verifica dell'invertibilità:** Prima di calcolare l'inversa, si verifica che il determinante della matrice sia coprimo con 26, condizione necessaria per l'esistenza dell'inversa modulare.
- **Uso di SymPy:** Poiché NumPy non supporta direttamente l'inversione modulare di matrici, si utilizza SymPy per questa operazione.

---

**Funzione known_plaintext_attack**

**Descrizione:**

Implementa un attacco con testo in chiaro noto per recuperare la matrice chiave, dato un testo in chiaro e il corrispondente testo cifrato.

**Passaggi principali:**

1. **Preprocessing dei testi:**    
    - Prepara sia il testo in chiaro che il testo cifrato.
2. **Divisione in blocchi:**    
    - Suddivide entrambi i testi in blocchi della lunghezza specificata della chiave.
3. **Creazione delle matrici:**    
    - Crea matrici quadrate dalle prime ( n ) lettere (dove ( n ) è la lunghezza della chiave) dei blocchi di testo in chiaro e cifrato.
4. **Calcolo dell'inversa del testo in chiaro:**    
    - Verifica che la matrice del testo in chiaro sia invertibile modulo 26.
    - Calcola l'inversa modulare della matrice del testo in chiaro.
5. **Calcolo della chiave:**    
    - Moltiplica la matrice del testo cifrato con l'inversa del testo in chiaro e applica il modulo 26: $K = (C \times P^{-1}) \mod 26$.
6. **Verifica della chiave:**    
    - Utilizza la chiave trovata per cifrare il testo in chiaro originale e confronta il risultato con il testo cifrato dato.

**Funzioni di libreria utilizzate:**

- ***sympy.Matrix.inv_mod():*** Calcola l'inversa modulare di una matrice.
- ***numpy.linalg.det():*** Calcola il determinante della matrice
- ***numpy.gcd()***: Determina se il determinante e il modulo sono coprimi.
- ***numpy.dot()***: Calcola il prodotto tra la matrici

---

### Considerazioni Generali 

- **Uso del Modulo 26:** Tutte le operazioni matematiche sono eseguite modulo 26 per rimanere all'interno dell'alfabeto inglese.
- **Preprocessing Consistente:** Tutte le funzioni iniziano con il preprocessing del messaggio per mantenere coerenza nei dati elaborati.
- **Gestione degli Errori:** Il codice include verifiche sull'invertibilità delle matrici e lancia eccezioni se le condizioni matematiche necessarie non sono soddisfatte.
