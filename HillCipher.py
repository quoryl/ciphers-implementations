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

def encrypt(message, key):
    message = preprocess_input(message)
    numbers = convert_to_numbers(message)
    key_length = len(key)
    blocks = get_blocks(numbers, key_length)

    rows = np.shape(key)[0]
    columns = np.shape(blocks)[1]

    # initialize the ciphertext matrix
    ciphertext = np.zeros((rows, columns)).astype(int)
    for i in range(columns):
        ciphertext[:, i] = np.reshape(np.dot(key, blocks[:, i]) % 26, rows)
    
    ciphertext_letters = np.zeros((rows, columns)).astype(str)
    for i in range(rows):
        for j in range(columns):
            ciphertext_letters[i, j] = chr(ciphertext[i, j] + 97)
   
    # Parameters
    # matrix: The input array to be flattened.
    # order: This parameter specifies the order in which the elements are read from the array. It can take the following values:
    # 'C' (default): Row-major (C-style) order.
    # 'F': Column-major (Fortran-style) order.
    # 'A': Fortran-style order if the array is Fortran contiguous in memory, C-style order otherwise.
    # 'K': Elements are read in the order they occur in memory, except for reversing the data when strides are negative.
    
    return "".join(np.ravel(ciphertext_letters, order='F'))

# Decryption
  
# P = C * K^-1 mod 26

def get_inverse(matrix, N):
    det = int(np.round(np.linalg.det(matrix))) % N   
    # check coprimality of det and N   
    if np.gcd(det, N) == 1:
        matrix = sympy_matrix(matrix)
        return np.matrix(matrix.inv_mod(N))
     # https://omz-software.com/pythonista/sympy/modules/matrices/matrices.html
    else:
        return None
    
def decrypt(message, key):
    message = preprocess_input(message)    
    N = 26
    key_inv = get_inverse(key, N)
    p = encrypt(message, key_inv)
    return p

def main():
    parser = argparse.ArgumentParser(
        description="Hill Cipher Encryption and Decryption",
        epilog="Example usage:\n"
               "  python HILLCIPHER.PY encrypt 'Your message here' '7,4;11,11'\n"
               "  python HILLCIPHER.PY decrypt 'Encrypted message here' '7,4;11,11'",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--mode", choices=["encrypt", "decrypt"], default="encrypt", help="Mode: encrypt or decrypt (default: encrypt)")
    parser.add_argument("--message", default="hello", help="The message to encrypt or decrypt (default: 'hello')")
    parser.add_argument("--key", default="7,4;11,11", help="The key matrix as a string, e.g., '7,4;11,11' for a 2x2 matrix (default: '7,4;11,11')")

    args = parser.parse_args()

    key = [list(map(int, row.split(','))) for row in args.key.split(';')]
    
    if verify_key_shape(key):
        key = np.array(key)
    else:
        raise ValueError("Key must be a square matrix")

    if args.mode == "encrypt":
        result = encrypt(args.message, key)
        print(f"Mode: {args.mode}")
        print(f"Message: {args.message}")
        print(f"Key: {args.key}")
        print(f"Encrypted message: {result}")
    elif args.mode == "decrypt":
        result = decrypt(args.message, key)
        print(f"Mode: {args.mode}")
        print(f"Message: {args.message}")
        print(f"Key: {args.key}")
        print(f"Decrypted message: {result}")

if __name__ == "__main__":
    main()