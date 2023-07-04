import nltk
from textblob import TextBlob

# Download necessary NLTK corpora
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def humanize_text(text):
    # Tokenize text into sentences
    sentences = nltk.sent_tokenize(text)

    # Iterate over each sentence and humanize it
    humanized_sentences = []
    for sentence in sentences:
        # Use TextBlob to get the part-of-speech tags for each word in the sentence
        tags = TextBlob(sentence).tags

        # Replace adjectives and adverbs with more human-like alternatives
        humanized_words = []
        for word, tag in tags:
            if tag.startswith('JJ'):
                humanized_words.append('amazing')
            elif tag.startswith('RB'):
                humanized_words.append('really')
            else:
                humanized_words.append(word)

        # Join the humanized words back into a sentence
        humanized_sentence = ' '.join(humanized_words)

        # Add the humanized sentence to the list of humanized sentences
        humanized_sentences.append(humanized_sentence)

    # Join the humanized sentences back into a single text
    humanized_text = ' '.join(humanized_sentences)

    return humanized_text

# Example usage
ai_generated_text = "The quick brown fox jumped over the lazy dog."
humanized_text = humanize_text(ai_generated_text)
print(humanized_text)