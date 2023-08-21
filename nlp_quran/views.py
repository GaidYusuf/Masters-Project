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

        # Construct absolute path for the trained model
        model_path = os.path.join(
            "/Users/qaayed/project/nlp_quran/", "doc2vec_model")

        # Load the trained Doc2Vec model
        model = Doc2Vec.load(model_path)

        # Preprocess user input and infer its vector
        preprocessed_input = preprocess_text(user_input)
        input_vector = model.infer_vector(word_tokenize(preprocessed_input))

        # Find most similar verses
        similar_verses = model.docvecs.most_similar([input_vector])

        # Return similar verses as JSON response
        response_data = {'similar_verses': similar_verses}
        return JsonResponse(response_data)

    return render(request, 'search.html')  # Render the search form
