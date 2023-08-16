# models.py
from django.db import models
import gensim
from gensim.models.doc2vec import Doc2Vec
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from typing import List, Tuple
import os

# Load the trained Doc2Vec model
doc2vec_model = Doc2Vec.load('/Users/qaayed/project/nlp_quran/doc2vec_model')

# Function to read data from the 'quran_data1.txt' file and create TaggedDocument objects


def read_data(filename):
    file_path = os.path.join(
        '/Users/qaayed/project/nlp_quran', filename)  # Absolute file path

    tagged_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the data and create tagged data using the verse ID as the tag and verse text as the words
        for line in file:
            if line.startswith('Verse ID:'):
                verse_id = line.strip().split(': ')[1]
                verse_text = next(file).strip().split(': ')[1]
                tagged_data.append(gensim.models.doc2vec.TaggedDocument(
                    words=verse_text.split(), tags=[verse_id]))

    return tagged_data

# Function to preprocess text (same as before)


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

# Function to infer embeddings for a given verse text


def infer_embedding(verse_text):
    verse_text = ' '.join(verse_text)  # Join the words into a single string
    preprocessed_text = preprocess_text(verse_text)
    inferred_vector = doc2vec_model.infer_vector(preprocessed_text.split())
    return inferred_vector

# Function to calculate cosine similarity between two vectors (same as before)


def cosine_similarity(vec1, vec2):
    vec1_dict = {i: float(val) for i, val in enumerate(vec1)}
    vec2_dict = {i: float(val) for i, val in enumerate(vec2)}
    return gensim.matutils.cossim(vec1_dict, vec2_dict)
