import spacy
from spacy import displacy
import input

nlp = spacy.load('en_core_web_lg')

def get_lemmatized_words(sentence):
    sentence = nlp(sentence)
    new_sentence = ''
    for word in sentence:
        new_sentence += word.lemma_ + ' '
    return new_sentence
