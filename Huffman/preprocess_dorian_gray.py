import string
import os

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

file_path = os.path.join(os.path.dirname(__file__), 'kafka.txt')
text = read_text_file(file_path)

def preprocess_text(text):
    # Remove anything that is not a standard English letter and make it lower case
    text = ''.join(filter(lambda c: c in string.ascii_letters, text)).lower()
    return text

preprocessed_text = preprocess_text(text)
output_file_path = os.path.join(os.path.dirname(__file__), 'preprocessed_kafka.txt')
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(preprocessed_text)
