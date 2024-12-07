import random

def miller_rabin(n, k=5):
    """
    Esegue il test di Miller-Rabin per verificare se n è probabilmente primo.
    
    Parametri:
    - n: numero da testare (deve essere >= 2).
    - k: numero di testimoni casuali da provare (default: 5).
    
    Ritorna:
    - True se n è probabilmente primo.
    - False se n è sicuramente composto.
    """
    # Caso base: numeri piccoli
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # Scomposizione di n-1 come 2^s * d con d dispari
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    
    # Funzione per testare un singolo testimone
    def is_composite(a):
        # Calcolo di a^d % n
        x = pow(a, d, n)  # Esponenziazione modulare
        if x == 1 or x == n - 1:
            return False  # a non è un testimone di compositeness
        # Calcola le potenze successive: a^(d*2^r) % n
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False  # a non è un testimone di compositeness
        return True  # a è un testimone di compositeness
    
    # Esegui il test per k testimoni casuali
    for _ in range(k):
        a = random.randint(2, n - 2)  # Scegli un testimone casuale
        if is_composite(a):
            return False  # Sicuramente composto
    
    return True  # Probabilmente primo

# # Esempio d'uso
# n = 117  # Numero da testare
# if miller_rabin(n, k=10):
#     print(f"{n} è probabilmente primo.")
# else:
#     print(f"{n} è sicuramente composto.")
