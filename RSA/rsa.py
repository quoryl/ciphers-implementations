import random
import time
import argparse

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
    # https://crypto.stackexchange.com/questions/2575/chinese-remainder-theorem-and-rsa
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


def main():
    parser = argparse.ArgumentParser(
        description="""RSA related algorithms

Commands:
  egcd                Extended Euclidean Algorithm
                      Parameters:
                        -a: First integer
                        -b: Second integer
                      Output: gcd, x, y
                      Example: python3 rsa.py egcd -a 240 -b 46

  modexp              Modular Exponentiation
                      Parameters:
                        -a: Base
                        -b: Exponent
                        -m: Modulus
                      Output: Result
                      Example: python3 rsa.py modexp -a 2 -b 10 -m 1000

  miller_rabin        Miller-Rabin Primality Test
                      Parameters:
                        -n: Number to test
                        -k: Number of rounds (default: 5)
                      Output: Is probably prime
                      Example: python3 rsa.py miller_rabin -n 17

  generate_prime      Generate Prime Number
                      Parameters:
                        -k: Number of bits
                      Output: Generated prime
                      Example: python3 rsa.py generate_prime -k 1024

  rsa_encrypt         RSA Encryption
                      Parameters:
                        -m: Message
                        -e: Public exponent
                        -n: Modulus
                      Output: Ciphertext
                      Example: python3 rsa.py rsa_encrypt -m 12345 -e 65537 -n 3233

  rsa_decrypt         RSA Decryption
                      Parameters:
                        -c: Ciphertext
                        -d: Private exponent
                        -n: Modulus
                      Output: Message
                      Example: python3 rsa.py rsa_decrypt -c 12345 -d 2753 -n 3233

  rsa_decrypt_crt     RSA Decryption with CRT
                      Parameters:
                        -c: Ciphertext
                        -p: Prime p
                        -q: Prime q
                        -dp: dp
                        -dq: dq
                        -qinv: qinv
                      Output: Message
                      Example: python3 rsa.py rsa_decrypt_crt -c 12345 -p 61 -q 53 -dp 17 -dq 29 -qinv 38

  generate_rsa_key    Generate RSA Key
                      Parameters:
                        -p: Prime p
                        -q: Prime q
                      Output: e, d, n
                      Example: python3 rsa.py generate_rsa_key -p 61 -q 53

  generate_rsa_crt_keys Generate RSA CRT Keys
                      Parameters:
                        -d: Private exponent
                        -p: Prime p
                        -q: Prime q
                      Output: dp, dq, qinv
                      Example: python3 rsa.py generate_rsa_crt_keys -d 2753 -p 61 -q 53

  test_rsa_times      Test RSA Times
                      Output: RSA average time, RSA CRT average time
                      Example: python3 rsa.py test_rsa_times
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    # Extended Euclidean Algorithm
    parser_egcd = subparsers.add_parser("egcd", help="Extended Euclidean Algorithm")
    parser_egcd.add_argument("-a", type=int, required=True, help="First integer")
    parser_egcd.add_argument("-b", type=int, required=True, help="Second integer")

    # Modular Exponentiation
    parser_modexp = subparsers.add_parser("modexp", help="Modular Exponentiation")
    parser_modexp.add_argument("-a", type=int, required=True, help="Base")
    parser_modexp.add_argument("-b", type=int, required=True, help="Exponent")
    parser_modexp.add_argument("-m", type=int, required=True, help="Modulus")

    # Miller-Rabin Primality Test
    parser_miller_rabin = subparsers.add_parser("miller_rabin", help="Miller-Rabin Primality Test")
    parser_miller_rabin.add_argument("-n", type=int, required=True, help="Number to test")
    parser_miller_rabin.add_argument("-k", type=int, default=5, help="Number of rounds")

    # Prime Number Generator
    parser_generate_prime = subparsers.add_parser("generate_prime", help="Generate Prime Number")
    parser_generate_prime.add_argument("-k", type=int, required=True, help="Number of bits")

    # RSA Encryption
    parser_rsa_encrypt = subparsers.add_parser("rsa_encrypt", help="RSA Encryption")
    parser_rsa_encrypt.add_argument("-m", type=int, required=True, help="Message")
    parser_rsa_encrypt.add_argument("-e", type=int, required=True, help="Public exponent")
    parser_rsa_encrypt.add_argument("-n", type=int, required=True, help="Modulus")

    # RSA Decryption
    parser_rsa_decrypt = subparsers.add_parser("rsa_decrypt", help="RSA Decryption")
    parser_rsa_decrypt.add_argument("-c", type=int, required=True, help="Ciphertext")
    parser_rsa_decrypt.add_argument("-d", type=int, required=True, help="Private exponent")
    parser_rsa_decrypt.add_argument("-n", type=int, required=True, help="Modulus")

    # RSA Decryption with CRT
    parser_rsa_decrypt_crt = subparsers.add_parser("rsa_decrypt_crt", help="RSA Decryption with CRT")
    parser_rsa_decrypt_crt.add_argument("-c", type=int, required=True, help="Ciphertext")
    parser_rsa_decrypt_crt.add_argument("-p", type=int, required=True, help="Prime p")
    parser_rsa_decrypt_crt.add_argument("-q", type=int, required=True, help="Prime q")
    parser_rsa_decrypt_crt.add_argument("-dp", type=int, required=True, help="dp")
    parser_rsa_decrypt_crt.add_argument("-dq", type=int, required=True, help="dq")
    parser_rsa_decrypt_crt.add_argument("-qinv", type=int, required=True, help="qinv")

    # Generate RSA Key
    parser_generate_rsa_key = subparsers.add_parser("generate_rsa_key", help="Generate RSA Key")
    parser_generate_rsa_key.add_argument("-p", type=int, required=True, help="Prime p")
    parser_generate_rsa_key.add_argument("-q", type=int, required=True, help="Prime q")

    # Generate RSA CRT Keys
    parser_generate_rsa_crt_keys = subparsers.add_parser("generate_rsa_crt_keys", help="Generate RSA CRT Keys")
    parser_generate_rsa_crt_keys.add_argument("-d", type=int, required=True, help="Private exponent")
    parser_generate_rsa_crt_keys.add_argument("-p", type=int, required=True, help="Prime p")
    parser_generate_rsa_crt_keys.add_argument("-q", type=int, required=True, help="Prime q")

    # Test RSA Times
    parser_test_rsa_times = subparsers.add_parser("test_rsa_times", help="Test RSA Times")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    elif args.command == "egcd":
        gcd, x, y = egcd(args.a, args.b)
        print(f"gcd: {gcd}, x: {x}, y: {y}")

    elif args.command == "modexp":
        result = binary_modular_exponentiation(args.a, args.b, args.m)
        print(f"Result: {result}")

    elif args.command == "miller_rabin":
        result = miller_rabin(args.n, args.k)
        print(f"Is probably prime: {result}")

    elif args.command == "generate_prime":
        prime = generate_prime(args.k)
        print(f"Generated prime: {prime}")

    elif args.command == "rsa_encrypt":
        ciphertext = rsa_encrypt(args.m, args.e, args.n)
        print(f"Ciphertext: {ciphertext}")

    elif args.command == "rsa_decrypt":
        message = rsa_decrypt(args.c, args.d, args.n)
        print(f"Message: {message}")

    elif args.command == "rsa_decrypt_crt":
        message = rsa_decrypt_crt(args.c, args.p, args.q, args.dp, args.dq, args.qinv)
        print(f"Message: {message}")

    elif args.command == "generate_rsa_key":
        e, d, n = generate_key(args.p, args.q)
        print(f"e: {e}, d: {d}, n: {n}")

    elif args.command == "generate_rsa_crt_keys":
        dp, dq, qinv = generate_crt_key(args.d, args.p, args.q)
        print(f"dp: {dp}, dq: {dq}, qinv: {qinv}")

    elif args.command == "test_rsa_times":
        test_rsa_times()

if __name__ == "__main__":
    main()