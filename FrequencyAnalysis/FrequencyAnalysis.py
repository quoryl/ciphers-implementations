import argparse
import json
import math
from collections import Counter
import matplotlib.pyplot as plt
import os
import string

def preprocess_text(text):
    # Remove punctuation, spaces, and convert to lowercase
    return text.translate(str.maketrans('', '', string.punctuation)).replace(' ', '').replace("\n", '').lower()

def index_of_coincidence_from_distribution(mgram_distribution):
    ic = sum( pow(q, 2) for q in mgram_distribution.values())
    return ic

def entropy(ngram_distribution):
    ent = -sum(f * math.log2(f) for f in ngram_distribution.values())
    return ent

def letter_frequency_histogram(text, output_path):
    text = preprocess_text(text)
    letter_counts = Counter(c for c in text if c.isalpha())
    letters = sorted(letter_counts.keys())
    frequencies = [letter_counts[letter] for letter in letters]
    letter_frequencies = zip(letters, frequencies)
    for l in letter_frequencies:
        print("Letter: ", l[0], "Frequency: ", l[1])

    plt.figure(figsize=(10, 6))
    plt.bar(letters, frequencies, color='plum')
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.title('Letter Frequency Histogram')
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()

def mgram_distribution_non_overlapping(text, m):
    if m < 1:
        print("Error: m should be greater than or equal to 1")
        return None

    text = preprocess_text(text)
    mgrams = [text[i:i+m] for i in range(0, len(text) - m + 1, m)]
    mgram_counts = Counter(mgrams)
    mgram_distribution = {mgram: mgram_counts[mgram] / len(mgrams) for mgram in mgram_counts}
    return mgram_distribution

def main():
    parser = argparse.ArgumentParser(
        description='Text Analysis Tool\n\n'
                    'Usage examples:\n'
                    '  python3 FrequencyAnalysis.py path/to/textfile.txt --histogram\n'
                    '    Calculate and plot the letter frequency histogram of the text.\n\n'
                    '  python3 FrequencyAnalysis.py path/to/textfile.txt --mgram 3\n'
                    '    Calculate the 3-gram empirical distribution of the text and plot the histogram.\n\n'
                    '  python3 FrequencyAnalysis.py path/to/textfile.txt --coincidence-entropy 3\n'
                    '    Compute the index of coincidence and entropy for the 3-gram empirical distribution of the text.\n'
                    '    The index of coincidence measures the likelihood of two randomly selected m-grams being identical.\n'
                    '    Entropy measures the randomness or unpredictability of the m-gram distribution.\n',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('file', type=str, help='Path to the text file')
    parser.add_argument('--histogram', action='store_true', help='Calculate and plot the letter frequency histogram')
    parser.add_argument('--mgram', type=int, dest='m', help='Calculate the m-gram empirical distribution')
    parser.add_argument('--coincidence-entropy', type=int, dest='m_gram_length', help='Compute index of coincidence and entropy of the empirical distribution')

    args = parser.parse_args()

    with open(args.file, 'r') as file:
        text = file.read()

    base_filename = os.path.splitext(os.path.basename(args.file))[0]

    if args.histogram:
        print("Calculating and plotting the letter frequency histogram...")
        output_path = f"{base_filename}_letter_frequency_histogram.png"
        letter_frequency_histogram(text, output_path)
        print(f"Letter frequency histogram saved to {output_path}")

    if args.m:
        m = args.m
        print(f"Calculating the {m}-gram empirical distribution...")
        distribution = mgram_distribution_non_overlapping(text, m)
        if distribution:
            output_path = f"{base_filename}_{m}gram_distribution.txt"
            with open(output_path, 'w') as output_file:    
                json.dump(distribution, output_file)
            print(f"N-gram empirical distribution saved to {output_path}")
        else:
            print("No distribution to display")

    if args.m_gram_length:
        m_gram_length = args.m_gram_length
        print(f"Computing index of coincidence and entropy for {m_gram_length}-gram empirical distribution...")
        distribution = mgram_distribution_non_overlapping(text, m_gram_length)
        if distribution:
            ic = index_of_coincidence_from_distribution(distribution)
            ent = entropy(distribution)
            print(f"Index of coincidence: {ic}")
            print(f"Entropy: {ent}")
        else:
            print("No distribution to display")

if __name__ == "__main__":
    main()