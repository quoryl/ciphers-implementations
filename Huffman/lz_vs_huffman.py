import huffman
import lempel_ziv
import os

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
probabilities = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

file_path = os.path.join(os.path.dirname(__file__), 'preprocessed_dorian_gray.txt')
text = read_text_file(file_path)

huffman_compression_ratios = []
lz78_compression_ratios = []

for i in range(0, 10):
    start_index = i * 1500
    end_index = start_index + 1500
    text_section = text[start_index:end_index]

    huffman_encoded = huffman.encode(chars, probabilities, text_section)
    lz78_encoded = lempel_ziv.lz78_encode(text_section)

    text_section_binary = ''.join(format(ord(char), '08b') for char in text_section)
    
    huffman_compression_ratio = (1-len(huffman_encoded) / len(text_section_binary));
    huffman_compression_ratios.append(huffman_compression_ratio)
    
    lz78_compression_ratio = (1-len(lz78_encoded) / len(text_section_binary));   
    lz78_compression_ratios.append(lz78_compression_ratio)


print("Average Huffman compression: ", sum(huffman_compression_ratios) / len(huffman_compression_ratios) * 100, "%")
print("Average LZ78 compression: ", sum(lz78_compression_ratios) / len(lz78_compression_ratios) * 100, "%")