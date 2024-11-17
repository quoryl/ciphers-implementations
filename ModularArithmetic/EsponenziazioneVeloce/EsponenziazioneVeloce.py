import sys
import argparse

def binary_modular_exponentiation(a, b, m):
    # this version is more readable but less efficient, it computes more results than needed
    # binary_representation = [int(c) for c in bin(b)[2:][::-1]]
    # indices = list(enumerate(binary_representation))

    # # a^b mod m
    # d = 1
    # for k, b_k in enumerate(binary_representation):
    #     if b_k == 1:
    #         # Calculate a^(2^k) % m (only for b_k == 1)
    #         local_result = pow(a, 2**k, m)
    #         d = (d * local_result) % m

    # return d

    result = 1
    a = a % m 
    while b > 0:
        if b % 2 == 1: # here we are checking if the last bit of b is 1, in that case we need to accumulate the result
            result = (result * a) % m
    
        a = (a * a) % m # deals with doubling the exponent of a at each iteration  
        b //= 2 # deals with the binary representation factor of b

    return result

def main():
    parser = argparse.ArgumentParser(description="Calculate (a^b) mod m using the binary modular exponentiation algorithm.")
    parser.add_argument('--base', type=int, required=True, help='The base number (a)')
    parser.add_argument('--exponent', type=int, required=True, help='The exponent (b)')
    parser.add_argument('--modulus', type=int, required=True, help='The modulus (m)')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    a = args.base
    b = args.exponent
    m = args.modulus

    result = binary_modular_exponentiation(a, b, m)
    print(f"The result of {a}^{b} mod {m} is: {result}")

if __name__ == "__main__":
    main()