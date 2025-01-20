import argparse


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
    input_string = "AABABBBABAABABBBABBABB"
    encoded_output = lz78_encode(input_string)
    print("Encoded output:", encoded_output)

    input = "0000000100001100000100000001010000001010000110000001001100000010000001"
    decoded_string = lz78_decode(input)
    print("Decoded output:", decoded_string)



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

if __name__ == "__main__":
    main()
