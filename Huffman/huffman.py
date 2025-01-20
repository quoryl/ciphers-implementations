import argparse
import heapq 
import string

class node: 
    def __init__(self, probability, symbol, left=None, right=None): 
        self.symbol = symbol 
        self.probability = probability        
        self.left = left 
        self.right = right
        self.encoded_value = '' 

    # overload smaller than operator
    def __lt__(self, next): 
        return self.probability < next.probability 

def walk_root(root):
    huffman_codes = {}
    stack = [(root, '')]
    while stack:
        node, code = stack.pop()
        new_code = code + str(node.encoded_value)
        if not node.left and not node.right:
            huffman_codes[node.symbol] = new_code
        if node.right:
            stack.append((node.right, new_code))
        if node.left:
            stack.append((node.left, new_code))

    is_valid = is_prefix_free(huffman_codes)
    # print("Is prefix-free: ", is_valid)
    return huffman_codes

def create_huffman_codes(symbols, probabilities):
    if not (0.99 <= sum(probabilities) <= 1.01):
        raise ValueError("Sum of probabilities must be approximately 1: sum(probabilities) = ", sum(probabilities))
    
    nodes = [] 
    for x in range(len(symbols)): 
        heapq.heappush(nodes, node(probabilities[x], symbols[x])) 
        
    while len(nodes) > 1: 
        left = heapq.heappop(nodes) 
        right = heapq.heappop(nodes) 

        left.encoded_value = 0
        right.encoded_value = 1
        
        parent = node(left.probability+right.probability, left.symbol+right.symbol, left, right)
        heapq.heappush(nodes, parent) 

    return walk_root(nodes[0])


def is_prefix_free(code):
    sorted_codes = sorted(code.values(), key=len)
    for i in range(len(sorted_codes)):
        for j in range(i + 1, len(sorted_codes)):
            if sorted_codes[j].startswith(sorted_codes[i]):
                return False
    return True

def decode(code, encoded_string):
    if not is_prefix_free(code):
        raise ValueError("The provided code is not prefix-free.")
    
    decoded_string = ''
    while encoded_string:
        for symbol, value in code.items():
            if encoded_string.startswith(value):
                decoded_string += symbol
                encoded_string = encoded_string[len(value):]
    return decoded_string

def encode(characters, probabilities, message):
        
    if not (len(characters) == len(probabilities)):
        raise ValueError("Length of characters and probabilities must be equal: len(characters) = ", len(characters), "len(probabilities) = ", len(probabilities))
    huffman_code = create_huffman_codes(characters, probabilities)
    # print(huffman_code)
    encoded_message = ''
    stripped_message = message.translate(str.maketrans('', '', string.punctuation)).replace(' ', '').replace("\n", '').lower()
    for char in stripped_message:
        encoded_message += huffman_code[char]
    return encoded_message

def run_demo():
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    probabilities = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

    print("Huffman encoding and decoding demo")
    print("Chars: ", chars)
    print("Probabilities: ", probabilities)
    print("Message: hello, world!")

    encoded_message = encode(chars, probabilities, 'hello, world!')
    print("Encoded message: ", encoded_message)

    decoded_message = decode(create_huffman_codes(chars, probabilities), encoded_message)
    print("Decoded message: ", decoded_message)

def main():
    parser = argparse.ArgumentParser(
        description="""Huffman encoding and decoding

Commands:
  create_huffman_code Create a Huffman code
                      Parameters:
                        -a: Alphabet (characters)
                        -p: Probabilities
                      Output: Huffman code (an optimal prefix free  code)
                      Example: python3 ./huffman.py create_huffman_code -a "a b c" -p "0.8 0.05 0.15"

  encode              Encode a message
                      Parameters:
                        -m: Message
                        -a: Alphabet (characters)
                        -p: Probabilities
                      Output: Encoded message
                      Example: python3 huffman.py encode -m "ccab" -a "a b c" -p "0.8 0.05 0.15"

  decode              Decode a message
                      Parameters:
                        -e: Encoded message (binary string)
                        -c: Prefix Free Code (not necessarily Huffman)
                      Output: Decoded message
                      Example: python3 huffman.py decode -e "0101100" -c "a: 1, b: 00, c: 01"      

  demo                Run demo
                      Output: Encoded and decoded hardcoded message : "hello, world!"
                      Example: python3 huffman.py demo
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    # Create Huffman Code
    parser_create_huffman_code = subparsers.add_parser("create_huffman_code", help="Create a Huffman code")
    parser_create_huffman_code.add_argument("-a", type=str, required=True, help="Alphabet (characters)")
    parser_create_huffman_code.add_argument("-p", type=str, required=True, help="Probabilities")

    # Encode
    parser_encode = subparsers.add_parser("encode", help="Encode a message")
    parser_encode.add_argument("-m", type=str, required=True, help="Message")
    parser_encode.add_argument("-a", type=str, required=True, help="Alphabet (characters)")
    parser_encode.add_argument("-p", type=str, required=True, help="Probabilities")

    # Decode
    parser_decode = subparsers.add_parser("decode", help="Decode a message")
    parser_decode.add_argument("-e", type=str, required=True, help="Encoded message (binary string)")
    parser_decode.add_argument("-c", type=str, required=True, help="Prefix Free Code (not necessarily Huffman)")

    # Demo
    subparsers.add_parser("demo", help="Run demo")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    elif args.command == "create_huffman_code":
        chars = args.a.split()
        probabilities = [float(x) for x in args.p.split()]
        huffman_code = create_huffman_codes(chars, probabilities)
        print(f"Huffman code: {huffman_code}")
    elif args.command == "encode":
        chars = args.a.split()
        probabilities = [float(x) for x in args.p.split()]
        message = args.m
        encoded_message = encode(chars, probabilities, message)
        print(f"Encoded message: {encoded_message}")
    elif args.command == "decode":
        code = {k: v for k, v in (item.split(": ") for item in args.c.split(", "))}
        encoded_message = args.e
        decoded_message = decode(code, encoded_message)
        print(f"Decoded message: {decoded_message}")
    elif args.command == "demo":
        run_demo()

if __name__ == "__main__":
    main()