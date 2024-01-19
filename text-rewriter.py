import nltk
from textblob import TextBlob
import re
from nltk.corpus import wordnet


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def replace_word(word, pos):
    synonyms = []
    for syn in wordnet.synsets(word, pos=pos):
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():
                synonyms.append(lemma.name())
    if synonyms:
        # Choose the most common synonym based on its frequency in the corpus
        freq_dist = nltk.FreqDist(synonyms)
        most_common_synonym = freq_dist.max()
        return most_common_synonym
    else:
        return word

def clean_symbols(humanized_text):
    # Remove extra spaces and unusual symbol placement
    humanized_text = re.sub(r'\s+', ' ', humanized_text)
    humanized_text = re.sub(r'\s([^\w\s])', r'\1', humanized_text)
    humanized_text = re.sub(r'([^\w\s])\s', r'\1', humanized_text)
    return humanized_text

def humanize_text(text):
    # Split text into sentences while preserving symbols
    # sentences = re.findall(r'[^.!?]+[.!?]+|[^\w\s]|\n', text)
    newline_placeholder = "庄周"
    text = text.replace('\n', newline_placeholder)

    sentences = re.findall(r'[^.!?]+[.!?]+|[^\w\s]+', text)

    # Iterate over each sentence and humanize it
    humanized_sentences = []
    for sentence in sentences:
        # Split sentence into words while preserving symbols
        words = re.findall(r'\w+|[^\w\s]+', sentence)

        # Use TextBlob to get the part-of-speech tags for each word in the sentence
        try:
            tags = TextBlob(sentence).tags
        except Exception as e:
            print(f"Error processing sentence: {e}")
            continue

        # Replace adjectives and adverbs with more human-like alternatives
        humanized_words = []
        for word, tag in tags:
            if tag.startswith('JJ'):
                humanized_word = replace_word(word, 'a')
                humanized_words.append(humanized_word)
            elif tag.startswith('RB'):
                humanized_word = replace_word(word, 'r')
                humanized_words.append(humanized_word)
            else:
                humanized_words.append(word)

        # Join the humanized words back into a sentence with symbols
        humanized_sentence = ''
        for i in range(len(words)):
            if words[i].isalpha() and i < len(humanized_words):
                humanized_sentence += humanized_words[i] + ' '
            else:
                humanized_sentence += words[i]

        humanized_sentences.append(humanized_sentence)


    # Join the humanized sentences back into a single text with symbols
    humanized_text = ''.join(humanized_sentences)

    humanized_text = clean_symbols(humanized_text)
    humanized_text = humanized_text.replace(newline_placeholder, '\n')

    return humanized_text.strip()

# Example usage
ai_generated_text = ""
print("here's the result!")
humanized_text = humanize_text(ai_generated_text)
print(humanized_text)
