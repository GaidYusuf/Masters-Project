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

# Function to preprocess text


def preprocess_text(text):
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


# API request
url = "http://api.alquran.cloud/v1/quran/en.asad"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Save the data to a text file after preprocessing
    with open('quran_data.txt', 'w', encoding='utf-8') as file:
        for surah in data['data']['surahs']:
            for verse in surah['ayahs']:
                verse_id = verse['number']
                verse_text = verse['text']
                preprocessed_text = preprocess_text(verse_text)
                file.write(f"Verse ID: {verse_id}\n")
                file.write(f"Original Text: {verse_text}\n")
                file.write(f"Preprocessed Text: {preprocessed_text}\n")
                file.write("=" * 50 + "\n")

    print("Data saved to 'quran_data.txt'.")

else:
    print("Failed to fetch data from the API.")
