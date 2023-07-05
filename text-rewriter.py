import nltk
from textblob import TextBlob
import re

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from nltk.corpus import wordnet

def replace_adjective(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():
                synonyms.append(lemma.name())
    if synonyms:
        return synonyms[0]
    else:
        return word

def replace_adverb(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():
                synonyms.append(lemma.name())
    if synonyms:
        return synonyms[0]
    else:
        return word

def humanize_text(text):
    # Split text into sentences while preserving symbols
    sentences = re.findall(r'[^.!?]+[.!?]+|[^\w\s]+', text)

    # Iterate over each sentence and humanize it
    humanized_sentences = []
    for sentence in sentences:
        # Split sentence into words while preserving symbols
        words = re.findall(r'\w+|[^\w\s]+', sentence)

        # Use TextBlob to get the part-of-speech tags for each word in the sentence
        tags = TextBlob(sentence).tags

        # Replace adjectives and adverbs with more human-like alternatives
        humanized_words = []
        for word, tag in tags:
            if tag.startswith('JJ'):
                humanized_word = replace_adjective(word)
                if humanized_word:
                    humanized_words.append(humanized_word)
                else:
                    humanized_words.append(word)
            elif tag.startswith('RB'):
                humanized_word = replace_adverb(word)
                if humanized_word:
                    humanized_words.append(humanized_word)
                else:
                    humanized_words.append(word)
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

    # Remove extra spaces and unusual symbol placement
    humanized_text = re.sub(r'\s+', ' ', humanized_text)
    humanized_text = re.sub(r'\s([^\w\s])', r'\1', humanized_text)
    humanized_text = re.sub(r'([^\w\s])\s', r'\1', humanized_text)

    return humanized_text.strip()

# Example usage
ai_generated_text = input("enter ai-generated text: ")
print("here's the result!")
humanized_text = humanize_text(ai_generated_text)
print(humanized_text)