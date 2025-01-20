import argparse
import os
import huffman

def lz78_decode(input_stream):
    dictionary = {0: ""}  
    dictionary_size = 1
    index_bits = 1
    char_bits = 5
    decoded_string = ""
    bit_pointer = 0

    while bit_pointer < len(input_stream):      
        index = int(input_stream[bit_pointer:bit_pointer + index_bits], 2)
        bit_pointer += index_bits

        char_code = int(input_stream[bit_pointer:bit_pointer + char_bits], 2)
        char = chr(char_code + ord('A'))
        bit_pointer += char_bits

        phrase = dictionary[index] + char
        decoded_string += phrase

        dictionary[dictionary_size] = phrase
        dictionary_size += 1

        if dictionary_size == (1 << index_bits):
            index_bits += 1

    return decoded_string


def lz78_encode(input_string):
    dictionary = {"": 0} 
    dictionary_size = 1
    index_bits = 1
    char_bits = 5 
    encoded_bits = ""
    current_phrase = ""

    for char in input_string:
        current_phrase += char
        if current_phrase not in dictionary:
            prefix_index = dictionary[current_phrase[:-1]]
            char_code = ord(current_phrase[-1]) - ord('A') 

            index_binary = f"{prefix_index:0{index_bits}b}"
            char_binary = f"{char_code:0{char_bits}b}"

            encoded_bits += index_binary + char_binary

            dictionary[current_phrase] = dictionary_size
            dictionary_size += 1

            # Check if we need to increase index bits
            if dictionary_size == (1 << index_bits):
                index_bits += 1

            # Reset current phrase, as it is now in the dictionary
            current_phrase = ""

    # Handle any remaining phrase
    # This is necessary if the input string ends with a phrase that is in the dictionary
    if current_phrase:
        prefix_index = dictionary[current_phrase[:-1]]
        char_code = ord(current_phrase[-1]) - ord('A')
        index_binary = f"{prefix_index:0{index_bits}b}"
        char_binary = f"{char_code:0{char_bits}b}"
        encoded_bits += index_binary + char_binary

    return encoded_bits

def run_demo():
    print("Demo of Lempel Ziv encoding and decoding")
    input_string = "AABABBBABAABABBBABBABB"
    encoded_output = lz78_encode(input_string)
    print("Encoded output:", encoded_output)

    input = "0000000100001100000100000001010000001010000110000001001100000010000001"
    decoded_string = lz78_decode(input)
    print("Decoded output:", decoded_string)

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def lz_vs_huffman():
    print("Comparing compression ratios of LZ78 and Huffman")
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    probabilities = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

    file_path = os.path.join(os.path.dirname(__file__), 'preprocessed_dorian_gray.txt')
    text = read_text_file(file_path)

    huffman_compression_ratios = []
    lz78_compression_ratios = []

    for i in range(0, 10):
        start_index = i * 1500
        end_index = start_index + 1500
        text_section = text[start_index:end_index]

        huffman_encoded = huffman.encode(chars, probabilities, text_section)
        lz78_encoded = lz78_encode(text_section)

        text_section_binary = ''.join(format(ord(char), '08b') for char in text_section)
        
        huffman_compression_ratio = (1-len(huffman_encoded) / len(text_section_binary));
        huffman_compression_ratios.append(huffman_compression_ratio)
        
        lz78_compression_ratio = (1-len(lz78_encoded) / len(text_section_binary));   
        lz78_compression_ratios.append(lz78_compression_ratio)


    print("Average Huffman compression: ", sum(huffman_compression_ratios) / len(huffman_compression_ratios) * 100, "%")
    print("Average LZ78 compression: ", sum(lz78_compression_ratios) / len(lz78_compression_ratios) * 100, "%")



def main():
    parser = argparse.ArgumentParser(
        description="""Lempel Ziv encoding and decoding

Commands:
encode              Encode a message
                    Parameters:
                    -m: Message
                    Output: Encoded message, in bits
                    Example: python3 lempel_ziv.py encode -m "AABABBBABAABABBBABBABB"

decode              Decode a message
                    Parameters:
                    -e: Encoded message (binary string)
                    Output: Decoded message, string
                    Example: python3 lempel_ziv.py decode -e "0000000100001100000100000001010000001010000110000001001100000010000001" 

demo                Run demo
                    Output: Encoded and decoded default message: "AABABBBABAABABBBABBABB"
                    Example: python3 lempel_ziv.py demo


lz_vs_huffman       Compare compression ratios of LZ78 and Huffman
                    Input: preprocessed_dorian_gray.txt, already in the same directory
                    Output: Average compression ratios of LZ78 and Huffman
                    Example: python3 lempel_ziv.py lz_vs_huffman
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    # Encode
    parser_encode = subparsers.add_parser("encode", help="Encode a message")
    parser_encode.add_argument("-m", type=str, required=True, help="Message")

    # Decode
    parser_decode = subparsers.add_parser("decode", help="Decode a message")
    parser_decode.add_argument("-e", type=str, required=True, help="Encoded message (binary string)")

    # Demo
    subparsers.add_parser("demo", help="Run demo")

    # Compare compression ratios of LZ78 and Huffman
    subparsers.add_parser("lz_vs_huffman", help="Compare compression ratios of LZ78 and Huffman")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    elif args.command == "encode":
        message = args.m
        encoded_message = lz78_encode(message)
        print(f"Encoded message: {encoded_message}")
    elif args.command == "decode":
        encoded_message = args.e
        decoded_message = lz78_decode(encoded_message)
        print(f"Decoded message: {decoded_message}")
    elif args.command == "demo":
        run_demo()
    elif args.command == "lz_vs_huffman":
        lz_vs_huffman()

if __name__ == "__main__":
    main()
