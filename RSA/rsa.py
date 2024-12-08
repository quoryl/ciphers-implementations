import random
import time


def egcd(a, b):
    x = 0    
    u = 1    
    y = 1
    v = 0    
    while a != 0:
        q = b // a
        r = b % a
        s = x - q * u
        t = y - q * v
        b = a
        a = r
        x = u
        y = v
        u = s
        v = t
    gcd = b
    return gcd, x, y

def binary_modular_exponentiation(a, b, m):
    result = 1
    a = a % m 
    while b > 0:
        if b % 2 == 1: # here we are checking if the last bit of b is 1, in that case we need to accumulate the result
            result = (result * a) % m
    
        a = (a * a) % m # deals with doubling the exponent of a at each iteration  
        b //= 2 # deals with the binary representation factor of b

    return result

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


def generate_prime(k, rounds=40):
    if k < 2:
        return None
    while True:
        number = generate_k_bit_number(k)
        if miller_rabin(number, rounds):
            return number
        

def generate_k_bit_number(k):
    # Generate a random number with k-2 bits (between 0 and 2^(k-2) - 1)
    # This will be the middle bits of the k-bit number
    # The MSB and LSB will be set to 1
    # k = 5, k-2 = 3, so the number should be between 000 and 111 > 0, 1, 2, 3, 4, 5, 6, 7, random.randint(0, 7)
    # 7 = 111 = 2^3 - 1 where 3 is k-2
    middle_bits = random.randint(0, (1 << (k - 2)) - 1)
    
    n = (1 << (k - 1)) | middle_bits | 1
    
    return n

# implementation of RSA algorithm
# two versions, with and without CRT

# RSA encryption E(m) = m^e mod n
# RSA decryption D(c) = c^d mod n

# I need to generate p,q, n, e, d, phi

# p,q are two large prime numbers
# n = p*q
# phi = (p-1)(q-1)
# e is a number that is coprime with phi
# d is the modular multiplicative inverse of e mod phi

def generate_key(p, q):
    n = p*q
    phi = (p-1)*(q-1)

    e = random.randint(2, phi-1)
    egcd_result = egcd(e, phi)

    while egcd_result[0] != 1:
        e = random.randint(2, phi-1)
        egcd_result = egcd(e, phi)

    d = pow(e, -1, phi)   
    return (e, d, n)

def generate_crt_key(d, p, q):
    # https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Using_the_Chinese_remainder_algorithm
    dp = d % (p-1)
    dq = d % (q-1)
    qinv = pow(q, -1, p)
    return (dp, dq, qinv)


def rsa_encrypt(m, e, n):
    return pow(m, e, n)   

def rsa_decrypt(c, d, n):
    return pow(c, d, n)

def rsa_decrypt_crt(c, p, q, dp, dq, qinv):
    m1 = pow(c, dp, p)
    m2 = pow(c, dq, q)
    h = (qinv * (m1 - m2)) % p
    return m2 + h*q

def test_rsa_times():
    prime_length = 1024
    p, q = generate_prime(prime_length), generate_prime(prime_length)
    e, d, n = generate_key(p, q)
    dp, dq, qinv = generate_crt_key(d, p, q)

    rsa_times = []
    rsa_crt_times = []

    for _ in range(100):
        c = random.getrandbits(prime_length)
        start = time.time()
        m = rsa_decrypt(c, d, n)
        rsa_times.append(time.time() - start)

        start = time.time()
        m2 = rsa_decrypt_crt(c, p, q, dp, dq, qinv)
        rsa_crt_times.append(time.time() - start)
    
    print("RSA average time: ", sum(rsa_times)/len(rsa_times))
    print("RSA CRT average time: ", sum(rsa_crt_times)/len(rsa_crt_times))


test_rsa_times()



