# views.py
from django.shortcuts import render
from .models import read_data, infer_embedding, cosine_similarity

# Function to handle similarity search


def similarity_search(request):
    verses = []  # List to store similar verses
    if request.method == 'POST':
        # Get the user-input verse text from the form
        user_input_verse = request.POST.get('verse_text', '')

        # Infer the embedding for the user-input verse using the Doc2Vec model
        user_embedding = infer_embedding(user_input_verse)

        # Load the Quranic verses from the 'quran_data1.txt' file
        tagged_data = read_data('quran_data1.txt')

        # Calculate the cosine similarity between the user-input verse and all verses
        similarity_scores = []
        for tagged_verse in tagged_data:
            verse_id = tagged_verse.tags[0]
            verse_text = tagged_verse.words
            verse_embedding = infer_embedding(verse_text)
            similarity_score = cosine_similarity(
                user_embedding, verse_embedding)
            similarity_scores.append((verse_text, verse_id, similarity_score))

        # Sort the verses based on their similarity scores in descending order
        similarity_scores.sort(key=lambda x: x[2], reverse=True)

        # Get the top N most similar verses
        N = 5  # Change this value to get more or fewer similar verses
        top_similar_verses = similarity_scores[:N]

        # Append the similar verses to the list for rendering in the template
        for verse_text, verse_id, similarity_score in top_similar_verses:
            verses.append((verse_text, verse_id, similarity_score))

    return render(request, 'nlp_quran/search.html', {'verses': verses})
