from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
from django.shortcuts import render
from django.http import JsonResponse
import os
import re
import nltk
from nltk.corpus import stopwords
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

    return ' '.join(words)


def similarity_search(request):
    if request.method == 'POST':
        user_input = request.POST.get('verse_input')

        # Construct absolute paths for the trained model and the translations file
        model_path = os.path.join(
            "/Users/qaayed/project/nlp_quran/", "doc2vec_model")
        translations_path = os.path.join(
            "/Users/qaayed/project/nlp_quran/", "quran_translations.txt")

        # Load the trained Doc2Vec model
        model = Doc2Vec.load(model_path)

        # Preprocess user input and infer its vector
        preprocessed_input = preprocess_text(user_input)
        input_vector = model.infer_vector(word_tokenize(preprocessed_input))

        # Find most similar verses
        similar_verses = model.docvecs.most_similar([input_vector])

        # Retrieve the corresponding Arabic text, translation, and verse
        with open(translations_path, 'r', encoding='utf-8') as translations_file:
            translations = {}
            current_verse = None
            arabic_text = None
            translation = None
            for line in translations_file:
                if line.startswith("Verse ("):
                    if current_verse is not None:
                        translations[current_verse] = {
                            'arabic_text': arabic_text,
                            'translation': translation
                        }
                    current_verse = line.strip()
                elif line.startswith("Arabic Text: "):
                    arabic_text = line[len("Arabic Text: "):].strip()
                elif line.startswith("Translation: "):
                    translation = line[len("Translation: "):].strip()

        # Prepare data for rendering in the template
        similar_verses_data = []
        for verse, similarity in similar_verses:
            data = translations.get(verse)
            if data:
                similar_verses_data.append({
                    'verse': verse,
                    'similarity': similarity,
                    'arabic_text': data['arabic_text'],
                    'translation': data['translation']
                })

        return render(request, 'search.html', {'similar_verses_data': similar_verses_data})

    return render(request, 'search.html')
