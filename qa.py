import input
import ner_tagging as ner
import spacy
import pos_tagging as pos
import lemma
import question_classification

nlp = spacy.load("en_core_web_lg")


def assign_question_type(question):
    types = []
    question_words = question.split()
    if (question_words[0] == 'Where'):
        types.append('GPE')
        types.append('NORP')
        types.append('LOC')
        types.append('FAC')
        types.append('EVENT')

    elif (question_words[0] == 'Who'):
        types.append('PERSON')
        types.append('ORG')
    elif (question_words[0] == 'When'):
        types.append('TIME')
        types.append('DATE')

    elif "how long" in question or "How long" in question:
        types.append('TIME')
        types.append('DATE')

    elif ('how many' in question or 'How many' in question):
        types.append('CARDINAL')
        types.append('QUANTITY')

    elif ('how far' in question or 'How far' in question):
        types.append('CARDINAL')
        types.append('QUANTITY')

    elif ('how small' in question or 'How small' in question) or ('how big' in question or 'How big' in question) or (
            'how tall' in question) or ('How tall' in question):
        types.append('QUANTITY')

    elif ('how old' in question or 'How old' in question):
        # types.append('CARDINAL')
        types.append('DATE')

    elif "how much" in question or "How much" in question:
        if 'cost' or 'price' or 'fee' or 'charge' or 'money' or 'rent' or 'fare' in question:
            types.append('MONEY')
        else:
            types.append('CARDINAL')
            types.append('QUANTITY')

    # elif "how often" in question or "How often" in question:
    #     types.append('TIME')
    #     types.append('DATE')

    # What, why, how, which,
    return types


# All possible answer sentences for the given question type
def get_text_with_type(story_id, types):
    answer_options = []
    for i in range(len(ner.all_story_tags[story_id])):
        sentence = ner.all_story_tags[story_id][i]
        for type in types:
            if type in sentence.values():
                answer_options.append(input.story_sentences[story_id][i])
                break
    return answer_options


# def subject_filter(question, story_id):
#     input_tags = {}
#     question_parse = nlp(question)
#     for word in question_parse:
#         input_tags[word.text] = word.dep_
#     subjects = []
#     for key in input_tags:
#         if 'nsubj' in input_tags.values():
#             subjects.append(key)

# sentences_list = []
# for curr_sentence in input.story_sentences[story_id]:
#     for sub in subjects:
#         if sub in curr_sentence:
#             sentences_list.append(curr_sentence)
# return sentences_list

def question_modulation(question):
    question = lemma.get_lemmatized_words(question)
    new_question = ''
    tagged_question = pos.get_input_tag(question)
    for word in tagged_question:
        if tagged_question[word] == 'NOUN':
            new_question += word + ' '
        elif tagged_question[word] == 'VERB':
            new_question += word + ' '
        elif tagged_question[word] == 'NUM':
            new_question += word + ' '
        elif tagged_question[word] == 'PROPN':
            new_question += word + ' '
        elif tagged_question[word] == 'ADJ':
            new_question += word + ' '
    return new_question


def similarity_question_modulation(question):
    question = lemma.get_lemmatized_words(question)
    new_question = ''
    tagged_question = pos.get_input_tag(question)
    for word in tagged_question:
        if tagged_question[word] == 'NOUN':
            new_question += word + ' '
        elif tagged_question[word] == 'VERB':
            new_question += word + ' '
        elif tagged_question[word] == 'ADV':
            new_question += word + ' '
        elif tagged_question[word] == 'NUM':
            new_question += word + ' '
        # elif tagged_question[word] == 'PROPN':
        #     new_question += word + ' '
        elif tagged_question[word] == 'ADJ':
            new_question += word + ' '
    return new_question


# find the overlap
def overlap(question, story_id):
    question = similarity_question_modulation(question)
    best_sentence = ''
    max_count = 0
    for curr_sentence in input.story_sentences[story_id]:
        count = 0
        ans_sentence = curr_sentence
        curr_sentence = lemma.get_lemmatized_words(curr_sentence)
        for s_word in curr_sentence.split():
            for q_word in question.split():
                if q_word == s_word:
                    count += 1
        if count > max_count:
            max_count = count
            best_sentence = ans_sentence
    return best_sentence


def remove_overlapped_words(question, answer_sentence):
    answer_sentence_set = set(answer_sentence.split())
    for word in question.split():
        if word in answer_sentence_set:
            answer_sentence_set.remove(word)
    answer_sentence = ''
    for word2 in answer_sentence_set:
        answer_sentence += word2 + ' '
    return answer_sentence


def filter_output(tags, types):
    final_answer = ''
    for each_tag in tags:
        if tags[each_tag] in types:
            final_answer += each_tag + " "
    return final_answer

def filter_quotes(answer):
    if "\"" in answer:
        first_index = answer.index("\"")
        if "\"" in answer[first_index + 1: ]:
            second_index = answer.index("\"", first_index + 1)
            return answer[first_index:second_index + 1]
    return ""

def subject_verb_similarity(question, story_id):
    question = lemma.get_lemmatized_words(question)
    question = nlp(question)
    q_sub = ""
    q_obj = ""
    q_verb = ""
    for word in question:
        if word.dep_ == "nsubj":
            q_sub = word.text
        elif word.dep_ == "ROOT":
            q_verb = word.text
        elif word.dep_ == "dobj":
            q_obj = word.text

    best_answer = ""
    for curr_sentence in input.story_sentences[story_id]:
        curr_sentence = lemma.get_lemmatized_words(curr_sentence)
        if q_verb != "be" and q_verb != "happen":
            if q_sub in curr_sentence and q_verb in curr_sentence:
                best_answer = curr_sentence
        # curr_sentence = nlp(curr_sentence)
        a_sub = ""
        a_obj = ""
        a_verb = ""
        # for word in curr_sentence:
        #     if word.dep_ == "nsubj":
        #         a_sub = word.text
        #     elif word.dep_ == "ROOT":
        #         a_verb = word.text
        #     elif word.dep_ == "dobj":
        #         a_obj = word.text
        # if q_sub == a_sub and q_verb == a_verb:
        #     best_answer == curr_sentence
        # if q_obj != "" and a_obj != "":
        #     if q_sub == a_sub and q_verb == a_verb and q_obj == a_obj:
        #         best_answer == curr_sentence

    return best_answer

def who_filter(question, story_id):
    answer = ""
    if "Who is" in question:
        question = question[6:]
        question = nlp(question)
        # count = 0
        bool = False
        for token in question.ents:
            # if count == 2:
            if token.label_ == "PERSON" or token.label_ == "ORG":
                bool = True
                break
        if bool:
            similarity = -1
            for answer_sentence in input.story_sentences[story_id]:
                lemma_sentence = lemma.get_lemmatized_words(answer_sentence)
                lemma_sentence = nlp(lemma_sentence)
                curr_similarity = lemma_sentence.similarity(question)
                if (similarity < curr_similarity):
                    answer = answer_sentence
                    similarity = curr_similarity
                # count += 1
    return answer

    # for token in question.ents:
    #     if token.label_ == "PERSON"

def find_most_similar_sentence(answer_options, question, story_id):
    # temp_answer = subject_verb_similarity(question, story_id)
    # if temp_answer != "":
    #     return temp_answer
    #     # answer_options.append(temp_answer)
    similarity = -1
    answer = ''
    # answer = who_filter(question, story_id)
    # if answer != "":
    #     answer_options.append(answer)
    new_question = question_modulation(question)
    new_question = nlp(new_question)
    sim_score = {}
    for answer_sentence in answer_options:
        lemma_sentence = lemma.get_lemmatized_words(answer_sentence)
        lemma_sentence = nlp(lemma_sentence)
        curr_similarity = lemma_sentence.similarity(new_question)
        sim_score[answer_sentence] = curr_similarity
        if (similarity < curr_similarity):
            answer = answer_sentence
            similarity = curr_similarity
    # If answer empty

    sim_ranked = {}
    sim_score = dict(sorted(sim_score.items(), key=lambda item: item[1]))
    count = 0
    for each_sentence in sim_score:
        sim_ranked[each_sentence] = count
        count += 1

    overlap_score = {}
    for answer_sentence in answer_options:
        count = 0
        ans_sentence = answer_sentence
        answer_sentence = lemma.get_lemmatized_words(answer_sentence)
        for s_word in answer_sentence.split():
            for q_word in new_question.text.split():
                if q_word == s_word:
                    count += 1
        overlap_score[ans_sentence] = count

    overlap_ranked = {}
    overlap_score = dict(sorted(overlap_score.items(), key=lambda item: item[1]))
    count = 0
    for each_sentence in overlap_score:
        overlap_ranked[each_sentence] = count
        count += 1

    best_score = -1
    sim_weight = 0.5
    overlap_weight = 0.5
    for each_sentence in sim_ranked:
        curr_score = sim_weight * sim_ranked[each_sentence] + overlap_weight * overlap_ranked[each_sentence]
        if curr_score > best_score:
            best_score = curr_score
            answer = each_sentence

    # WHAT WHY HOW
    if len(answer_options) == 0:
        # if "How" in question:
        #     new_question = question_modulation(question)
        #     new_question = nlp(new_question)
        #     # SIMILARITY
        #     sim_score = {}
        #     for answer_sentence in input.story_sentences[story_id]:
        #         lemma_sentence = lemma.get_lemmatized_words(answer_sentence)
        #         lemma_sentence = nlp(lemma_sentence)
        #         curr_similarity = lemma_sentence.similarity(new_question)
        #         sim_score[answer_sentence] = curr_similarity
        #         if (similarity < curr_similarity):
        #             answer = answer_sentence
        #             similarity = curr_similarity
        #     # RANK SIMILARITY
        #     sim_ranked = {}
        #     sim_score = dict(sorted(sim_score.items(), key=lambda item: item[1]))
        #     count = 0
        #     for each_sentence in sim_score:
        #         sim_ranked[each_sentence] = count
        #         count += 1
        #     # OVERLAP
        #     overlap_score = {}
        #     for answer_sentence in input.story_sentences[story_id]:
        #         count = 0
        #         ans_sentence = answer_sentence
        #         answer_sentence = lemma.get_lemmatized_words(answer_sentence)
        #         for s_word in answer_sentence.split():
        #             for q_word in new_question.text.split():
        #                 if q_word == s_word:
        #                     count += 1
        #         overlap_score[ans_sentence] = count
        #     # RANK OVERLAP
        #     overlap_ranked = {}
        #     overlap_score = dict(sorted(overlap_score.items(), key=lambda item: item[1]))
        #     count = 0
        #     for each_sentence in overlap_score:
        #         overlap_ranked[each_sentence] = count
        #         count += 1
        #
        #     # WEIGHT
        #     best_score = -1
        #     sim_weight = 0.2
        #     overlap_weight = 0.8
        #     for each_sentence in sim_ranked:
        #         curr_score = sim_weight * sim_ranked[each_sentence] + overlap_weight * overlap_ranked[each_sentence]
        #         if curr_score > best_score:
        #             best_score = curr_score
        #             answer = each_sentence

        if "What type of" in question or "What kind of" in question:
            potential_answers = []
            new_question = nlp(question)
            pobj = ""
            for token in new_question:
                if token.dep_ == "pobj":
                    pobj = token.text
                    break
            for answer_sentence in input.story_sentences[story_id]:
                if pobj in answer_sentence:
                    potential_answers.append(answer_sentence)
            for x in potential_answers:
                x = nlp(x)
                curr_similarity = x.similarity(new_question)
                if (similarity < curr_similarity):
                    answer = x.text
                    similarity = curr_similarity
            answer = remove_overlapped_words(question, answer)

        else:
            answer = overlap(question, story_id)

        if "What is the name" in question:
            tags = pos.get_input_tag(answer)
            types = ["PROPN"]
            answer = filter_output(tags, types) + filter_quotes(answer)
        elif "At whose" in question or "at whose" in question:
            tags = pos.get_input_tag(answer)
            types = ["PROPN"]
            answer = filter_output(tags, types)
        elif "What age" in question or "What is the age" in question:
            tags = ner.get_input_tag(answer)
            types = ["CARDINAL"]
            answer = filter_output(tags, types)
        else:
            answer = remove_overlapped_words(question, answer)
    return answer


for story_id in input.question_data:
    for question_id in input.question_data[story_id]:
        question_type = ''
        question = input.question_data[story_id][question_id][0]
        types = assign_question_type(question)
        if (len(types) == 0):
            types = question_classification.get_answer_type(question)
        answer_options = get_text_with_type(story_id, types)
        answer = find_most_similar_sentence(answer_options, question, story_id)
        final_answer = answer

        question_words = question.split()
        tags = ner.get_input_tag(answer)
        if (question_words[0] == 'Where'):
            types = ['GPE', 'FAC', 'NORP', 'LOC', 'EVENT']
            final_answer = filter_output(tags, types)

        elif (question_words[0] == 'Who'):
            types = ['PERSON', 'ORG']
            final_answer = filter_output(tags, types)

        elif (question_words[0] == 'When'):
            types = ['TIME', 'DATE']
            final_answer = filter_output(tags, types)

        elif "how long" in question or "How long" in question:
            types = ['TIME', 'DATE']
            final_answer = filter_output(tags, types)
            if ('-' in final_answer):
                final_answer = final_answer.replace('-', ' ')

        elif ('how many' in question or 'How many' in question):
            types = ['CARDINAL', 'QUANTITY']
            final_answer = filter_output(tags, types)
            if ('-' in final_answer):
                final_answer = final_answer.replace('-', ' ')

        elif ('how far' in question or 'How far' in question):
            types = ['CARDINAL', 'QUANTITY']
            final_answer = filter_output(tags, types)
            if ('-' in final_answer):
                final_answer = final_answer.replace('-', ' ')

        elif "how old" in question or "How old" in question:
            final_answer = filter_output(tags, types)
            if ('-' in final_answer):
                final_answer = final_answer.replace('-', ' ')

        elif ('how small' in question or 'How small' in question) or (
                'how big' in question or 'How big' in question) or (
                'how tall' in question) or ('How tall' in question):
            types = ['QUANTITY']
            final_answer = filter_output(tags, types)
            if ('-' in final_answer):
                final_answer = final_answer.replace('-', ' ')

        elif "how much" in question or "How much" in question:
            if 'cost' or 'price' or 'fee' or 'charge' or 'money' or 'rent' or 'fare' in question:
                types = ['MONEY']
                final_answer = filter_output(tags, types)

            else:
                types = ['CARDINAL', 'QUANTITY']
                final_answer = filter_output(tags, types)
        else:
            types = question_classification.answer_trimming(question, answer)
            final_answer = filter_output(tags, types)

        if len(final_answer) == 0:
            final_answer = answer
        final_answer = final_answer.strip()
        fna = ''
        for word in final_answer.split():
            if word == '\n':
                continue
            fna += word + ' '

        print("QuestionID: " + question_id)
        print("Answer: ", fna)
        print()

