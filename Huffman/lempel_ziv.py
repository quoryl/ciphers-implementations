def lz78_decode(input_stream):
    dictionary = {0: ""}  # Initialize dictionary with empty string
    dictionary_size = 1
    index_bits = 1
    char_bits = 5
    decoded_string = ""
    bit_pointer = 0

    while bit_pointer < len(input_stream):
        # Read index
        index = int(input_stream[bit_pointer:bit_pointer + index_bits], 2)
        bit_pointer += index_bits

        # Read character
        char_code = int(input_stream[bit_pointer:bit_pointer + char_bits], 2)
        char = chr(char_code + ord('A'))
        bit_pointer += char_bits

        # Process the (index, char) pair
        phrase = dictionary[index] + char
        decoded_string += phrase

        # Update dictionary
        dictionary[dictionary_size] = phrase
        dictionary_size += 1

        # Check if we need to increase index bits
        if dictionary_size == (1 << index_bits):
            index_bits += 1

    return decoded_string


def lz78_encode(input_string):
    dictionary = {"": 0}  # Initialize dictionary with empty string at index 0
    dictionary_size = 1
    index_bits = 1
    char_bits = 5  # Fixed 5 bits for characters (A-Z)
    encoded_bits = ""
    current_phrase = ""

    for char in input_string:
        current_phrase += char
        if current_phrase not in dictionary:
            # Encode the index of the longest prefix and the new character
            prefix_index = dictionary[current_phrase[:-1]]
            char_code = ord(current_phrase[-1]) - ord('A')  # Convert character to 5-bit code

            # Convert index and character to binary strings
            index_binary = f"{prefix_index:0{index_bits}b}"
            char_binary = f"{char_code:0{char_bits}b}"

            # Append to the encoded bit stream
            encoded_bits += index_binary + char_binary

            # Add the new phrase to the dictionary
            dictionary[current_phrase] = dictionary_size
            dictionary_size += 1

            # Check if we need to increase index bits
            if dictionary_size == (1 << index_bits):
                index_bits += 1

            # Reset current phrase
            current_phrase = ""

    # Handle any remaining phrase
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
    print(encoded_output)

    # Example usage
    input = "0000000100001100000100000001010000001010000110000001001100000010000001"
    decoded_string = lz78_decode(input)
    print(decoded_string)

# run_demo()