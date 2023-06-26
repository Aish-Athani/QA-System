import spacy
from spacy import displacy
import input

nlp = spacy.load('en_core_web_sm')
story_tags = {}
for story in input.story_data:
    doc = nlp(input.story_data[story][3])
    story_tags[story] = doc

story_sentence_tags = []
for story in input.story_sentences:
    for sentence in input.story_sentences[story]:
        story_sentence_tags.append(nlp(sentence))

question_tags = {}
for story in input.question_data:
    each_story_qtags = {}
    for question_id in input.question_data[story]:
        question = input.question_data[story][question_id]
        doc = nlp(question[1])
        each_story_qtags[question_id] = doc
    question_tags[story] = each_story_qtags

sentence_tags = []
for sentence in story_sentence_tags:
    word_tags = {}
    for word in sentence:
        # print(word.text, word.pos_)
        word_tags[word.text] = word.pos_
    sentence_tags.append(word_tags)
