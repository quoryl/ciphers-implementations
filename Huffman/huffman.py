# A Huffman Tree Node 
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
    print("Is prefix-free: ", is_valid)
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
    print(huffman_code)
    encoded_message = ''
    stripped_message = message.translate(str.maketrans('', '', string.punctuation)).replace(' ', '').replace("\n", '').lower()
    for char in stripped_message:
        encoded_message += huffman_code[char]
    return encoded_message

def run_demo():
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    probabilities = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

    encoded_message = encode(chars, probabilities, 'hello, world!')
    print(encoded_message)

    decoded_message = decode(create_huffman_codes(chars, probabilities), encoded_message)
    print(decoded_message)


run_demo()


