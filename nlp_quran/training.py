import gensim
from gensim.models.doc2vec import TaggedDocument

# Function to read data from the file and create TaggedDocument objects


def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n\n')  # Split based on the newline character

    tagged_data = []
    for line in lines:
        verse_data = line.strip().split('\n')
        verse_id = int(verse_data[0].split(':')[-1])
        verse_text = verse_data[1].split(': ')[1]  # Extract the verse text
        tagged_data.append(TaggedDocument(verse_text.split(), [str(verse_id)]))

    return tagged_data


# Load the preprocessed data
tagged_data = read_data('quran_data.txt')

# Train the Doc2Vec model
model = gensim.models.Doc2Vec(
    vector_size=50, window=2, min_count=2, workers=4, epochs=10)
model.build_vocab(tagged_data)
model.train(tagged_data, total_examples=model.corpus_count,
            epochs=model.epochs)

# Save the trained model
model.save('doc2vec_model')

print("Doc2Vec model trained and saved successfully.")
