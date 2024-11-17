import sys
import argparse

def binary_modular_exponentiation(a, b, m):
    binary_representation = [int(c) for c in bin(b)[2:][::-1]]
    indices = list(enumerate(binary_representation))

    # a^b mod m
    d = 1
    for k in indices:
        two_power_k = pow(2, k[0]) * k[1] # 2^k * b_k    
        local_result = pow(a, two_power_k, m) # a^(2^k * b_k) mod m
        d = (d * local_result) % m

    return d

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