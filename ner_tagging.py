import spacy
from spacy import displacy
import input

nlp = spacy.load('en_core_web_lg')
story_tags = {}

# NER TAGGING
all_story_tags = {}
for story in input.story_sentences:
    story_sentence_tags = []
    for sentence in input.story_sentences[story]:
        story_sentence_tags.append(nlp(sentence))
   
    sentence_tags = []
    for sentence in story_sentence_tags:
        word_tags = {}
        for word in sentence.ents:
            word_tags[word.text] = word.label_
        sentence_tags.append(word_tags)
    all_story_tags[story] = sentence_tags


question_tags = {}
for story in input.question_data:
    each_story_qtags = {}
    for question_id in input.question_data[story]:
        question = input.question_data[story][question_id]
        doc = nlp(question[0])
        each_story_qtags[question_id] = doc
    question_tags[story] = each_story_qtags

questions = {}
for story_id in question_tags:
    question_tagging = {}
    for question in question_tags[story_id]:
        word_tags = {}
        for word in question_tags[story_id][question].ents:
            word_tags[word.text] = word.label_
        question_tagging[question] = word_tags
    questions[story_id] = question_tagging

def get_input_tag(sentence):
    input_tags = {}
    sentence = nlp(sentence)
    for word in sentence.ents:
        input_tags[word.text] = word.label_
    return input_tags