from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

# Read the preprocessed verses data
input_file_path = 'preprocessed_quran_translations.txt'

# Prepare tagged documents for training
tagged_data = []
current_tags = None
current_text = ""
with open(input_file_path, 'r', encoding='utf-8') as input_file:
    for line in input_file:
        if line.startswith("Verse ("):
            current_tags = line.strip()
            current_text = ""
        elif line.startswith("Preprocessed Translation: "):
            current_text = line[len("Preprocessed Translation: "):]
            tagged_data.append(TaggedDocument(
                words=word_tokenize(current_text), tags=[current_tags]))

# Define Doc2Vec model configuration
vector_size = 300  # Size of the resulting vector (embedding)
window = 5  # Maximum distance between the current and predicted word within a sentence
min_count = 2  # Ignores all words with total frequency lower than this
workers = 4  # Number of CPU cores to use when training the model

# Initialize and train the Doc2Vec model
model = Doc2Vec(vector_size=vector_size, window=window,
                min_count=min_count, workers=workers)
model.build_vocab(tagged_data)
model.train(tagged_data, total_examples=model.corpus_count,
            epochs=30)  # Adjust epochs as needed

# Save the trained model
model.save("doc2vec_model")

print("Doc2Vec model trained and saved.")
