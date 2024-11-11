import argparse
import math
import string
from sympy import Matrix as sympy_matrix
import numpy as np

# Message representation

def preprocess_input(message):
    message_lower = message.lower().replace(" ", "")
    # Remove punctuation from the message
    message_clean = message_lower.translate(str.maketrans('', '', string.punctuation))
    return message_clean

def convert_to_numbers(message):
    # Convert the message to numbers,
    # where a = 0, b = 1, ..., z = 25
    # ord('a') = 97
    return [ord(char) - 97 for char in message]


def get_blocks(message, key_length):
    while len(message) % key_length != 0:
        message.append(25)
    
    rows = int(len(message) / key_length)
    columns = key_length
    block_shape = (rows, columns)
    return np.reshape(message, block_shape).transpose()
      

# Encryption
 # C = P * K mod 26

def verify_key_shape(key):
    # Check if the key is square
    if len(key) != len(key[0]):
        raise ValueError("Key must be a square matrix")
    else:
        return True

def encrypt(message, key, N):
    message = preprocess_input(message)
    numbers = convert_to_numbers(message)
    key_length = len(key)
    blocks = get_blocks(numbers, key_length)

    rows = np.shape(key)[0]
    columns = np.shape(blocks)[1]

    # initialize the ciphertext matrix
    ciphertext = np.zeros((rows, columns)).astype(int)
    for i in range(columns):
        ciphertext[:, i] = np.reshape(np.dot(key, blocks[:, i]) % N, rows)
    
    ciphertext_letters = np.zeros((rows, columns)).astype(str)
    for i in range(rows):
        for j in range(columns):
            ciphertext_letters[i, j] = chr(ciphertext[i, j] + 97)
   
    # 'F': Column-major (Fortran-style) order. 
    # Specifies the order in which the elements are read from the array
    return "".join(np.ravel(ciphertext_letters, order='F'))

# Decryption  
# P = C * K^-1 mod 26

def get_inverse(matrix, N):
    det = int(np.round(np.linalg.det(matrix))) % N   
    # check coprimality of det and N   
    if np.gcd(det, N) == 1:
        matrix = sympy_matrix(matrix)
        return np.matrix(matrix.inv_mod(N))
    else:
        return None
    
def decrypt(message, key, N):
    message = preprocess_input(message)    
    key_inv = get_inverse(key, N)
    p = encrypt(message, key_inv, N)
    return p


# Known Plaintext Attack
# P = C * P^-1 mod 26

def verify_key(plaintext, ciphertext, key_matrix, N):
    print("Key verification in progress...")

    plaintext = preprocess_input(plaintext)
    ciphertext = preprocess_input(ciphertext)

    test_ciphertext = encrypt(plaintext, key_matrix, N)    
    print("Original ciphertext:", ciphertext)
    print("Ciphertext computed with the extracted key:", test_ciphertext)

    if test_ciphertext == ciphertext:
        print("Key verification successful.")
    else:
        print("Key verification failed.")

def known_plaintext_attack(plaintext, ciphertext, key_length, N):
    plaintext = preprocess_input(plaintext)
    ciphertext = preprocess_input(ciphertext)

    p_blocks = get_blocks(convert_to_numbers(plaintext), key_length)
    c_blocks = get_blocks(convert_to_numbers(ciphertext), key_length)

    # Extract square matrices
    p_square = p_blocks[:key_length, :key_length]
    c_square = c_blocks[:key_length, :key_length]

    det_p = int(np.round(np.linalg.det(p_square))) % N
    if np.gcd(det_p, N) != 1:
        raise ValueError("The plaintext matrix is not invertible.")
    
    p_inverse = get_inverse(p_square, N)

    if p_inverse is None:
        raise ValueError("The plaintext matrix is not invertible.")
    
    key_matrix = np.dot(c_square, p_inverse) % N  
    return key_matrix

def main():
    parser = argparse.ArgumentParser(
        description="Hill Cipher Encryption, Decryption, and Known Plaintext Attack",
        epilog="Example usage:\n"
               "  python3 HillCipher.py --mode encrypt --message 'Your message here' --key '7,4;11,11'\n"
               "  python3 HillCipher.py --mode decrypt --message 'Encrypted message here' --key '7,4;11,11'\n"
               "  python3 HillCipher.py --mode known-plaintext-attack --plaintext 'Your plaintext here' --ciphertext 'Your ciphertext here' --key-length 2",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--mode", choices=["encrypt", "decrypt", "known-plaintext-attack"], default="encrypt", help="Mode: encrypt, decrypt, or known-plaintext-attack (default: encrypt)")
    parser.add_argument("--message", help="The message to encrypt or decrypt")
    parser.add_argument("--key", help="The key matrix as a string, e.g., '7,4;11,11' for a 2x2 matrix")
    parser.add_argument("--plaintext", type=str, default="HELP", help="Plaintext for known plaintext attack (default: 'HELP')")
    parser.add_argument("--ciphertext", type=str, default="TQXX", help="Ciphertext for known plaintext attack (default: 'TQXX')")
    parser.add_argument("--key-length", type=int, help="The length of the key matrix")

    args = parser.parse_args()

    N = 26

    if args.mode in ["encrypt", "decrypt"]:
        if not args.message or not args.key:
            raise ValueError("Both message and key must be provided for encryption or decryption.")
        key = [list(map(int, row.split(','))) for row in args.key.split(';')]
        if verify_key_shape(key):
            key = np.array(key)
        else:
            raise ValueError("Key must be a square matrix")

    if args.mode == "known-plaintext-attack":
        if not args.key_length:
            if args.key:
                key_length = int(math.sqrt(len(args.key.split(';'))))
            else:
                raise ValueError("Key length must be provided for known plaintext attack.")
        else:
            key_length = args.key_length
        key_matrix = known_plaintext_attack(args.plaintext, args.ciphertext, key_length, N)
        print("Key:")
        print(key_matrix)

        verify_key(args.plaintext, args.ciphertext, key_matrix, N)
        
    elif args.mode == "encrypt":
        result = encrypt(args.message, key, N)
        print(f"Mode: {args.mode}")
        print(f"Message: {args.message}")
        print(f"Key: {args.key}")
        print(f"Encrypted message: {result}")
    elif args.mode == "decrypt":
        result = decrypt(args.message, key, N)
        print(f"Mode: {args.mode}")
        print(f"Message: {args.message}")
        print(f"Key: {args.key}")
        print(f"Decrypted message: {result}")

if __name__ == "__main__":
    main()