import random
import MillerRabin

def generate_prime(k, rounds=40):
    if k < 2:
        return None
    while True:
        number = generate_k_bit_number(k)
        if MillerRabin.miller_rabin(number, rounds):
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
