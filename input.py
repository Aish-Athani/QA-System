import sys
import spacy
nlp = spacy.load("en_core_web_lg")

def read_question_file(file_name):
    question_data = {}
    count = 0
    question_id = ""
    question_text = ""
    difficulty = ""
    with open(file_name, "r") as file:
        for line in file:
            if count == 0:
                question_id = line[12:].strip()
            if count == 1:
                question_text = line[10:].strip()
            if count == 2:
                difficulty = line[12:].strip()
            if line == "\n" and count != 0:
                count = 0
                question_data[question_id] = (question_text, difficulty)
                continue
            count += 1
    return question_data

def read_story_file(file_name):
    story_data = [""] * 4
    text = ""
    count = 0
    with open(file_name, "r") as file:
        for line in file:
            if count == 0:
                story_data[0] = line[10:].strip()
            if count == 1:
                story_data[1] = line[6:].strip()
            if count == 2:
                story_data[2] = line[9:].strip()
            if count > 5:
                text += line
            count += 1
    story_data[3] = text
    return story_data


def sentence_splitter(story_data):
    story_data_sentences = {}
    for story in story_data:
        sentences = []
        story_id = story_data[story][2]
        story_text = nlp(story_data[story][3])
        for sent in story_text.sents:
            sentences.append(sent.text)
        story_data_sentences[story_id] = sentences
    return story_data_sentences

input_file_name = sys.argv[1]

story_ids = []
path = ''
with open(input_file_name, "r") as input_file:
    count = 0
    for line in input_file:
        if count == 0:
            path = line.strip()
        else:
            story_ids.append(line)
        count += 1

story_data = {}
question_data = {}
story_sentences = {}
for id in story_ids:
    id = id.strip()
    story_file_name = path + id + ".story"
    question_file_name = path + id + ".questions"
    story_data[id] = read_story_file(story_file_name)
    question_data[id] = read_question_file(question_file_name)


story_sentences = sentence_splitter(story_data)



