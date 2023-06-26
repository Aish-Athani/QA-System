import spacy
from spacy import displacy
import input

nlp = spacy.load('en_core_web_lg')

def get_input_tag(sentence):
    input_tags = {}
    sentence = nlp(sentence)
    for word in sentence:
        input_tags[word.text] = word.pos_
    return input_tags
