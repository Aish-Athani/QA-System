import input
import sense_new

question_answers = {}
for story_id in sense_new.question_senses:
    answer_list = []
    answer_sentence_index = 0
    for question in sense_new.question_senses[story_id]:
        # each_question_senses = sense_new.question_senses[story_id]
        sentence_index = 0
        max_count = 0
        for sentence in sense_new.story_senses:
            # START COMPARSION ALGORITHM
            count = 0
            for story_word in sentence:
                for question_word in question:
                    if sentence[story_word] == question[question_word]:
                        count += 1
            if count >= max_count:
                max_count = count
                answer_sentence_index = sentence_index
            sentence_index += 1
        answer_list.append(answer_sentence_index)
    question_answers[story_id] = answer_list

for story_id in input.story_sentences:
    for answer in question_answers[story_id]:
        print(input.story_sentences[story_id][answer])
        print()