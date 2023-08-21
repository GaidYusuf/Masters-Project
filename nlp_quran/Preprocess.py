from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import re
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Download NLTK resources if not already present
nltk.download('punkt')
nltk.download('stopwords')

# Function to preprocess English translation text


def preprocess_translation_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove special characters and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenize text into individual words
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Perform stemming using Porter Stemmer
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    return ' '.join(words)


# Read the input file containing translations
input_file_path = 'quran_translations.txt'
output_file_path = 'preprocessed_quran_translations.txt'

with open(input_file_path, 'r', encoding='utf-8') as input_file:
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        arabic_text = ""
        for line in input_file:
            if line.startswith("Verse ("):
                arabic_text = ""  # Reset the Arabic text when a new verse starts
                output_file.write(line)  # Write the original verse line
            elif line.startswith("Arabic Text: "):
                arabic_text = line[len("Arabic Text: "):]
            elif line.startswith("Translation: "):
                translation = line[len("Translation: "):]
                preprocessed_translation = preprocess_translation_text(
                    translation)

                output_file.write(f"Arabic Text: {arabic_text}\n")
                output_file.write(f"English Translation: {translation}")
                output_file.write(
                    f"Preprocessed Translation: {preprocessed_translation}\n")
                output_file.write("=" * 50 + "\n")

print("Preprocessing complete. Preprocessed data saved to 'preprocessed_quran_translations.txt'.")
