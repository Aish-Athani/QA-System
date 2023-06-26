from nltk.corpus import wordnet as wn
import input
from nltk.corpus import stopwords
stopwords_set = stopwords.words('english')

def remove_stopwords(words_set):
    new_words_set = words_set.copy()
    for word in words_set:
        word_lower = word.lower()
        if word_lower in stopwords_set:
            new_words_set.remove(word)
            continue
        if not word_lower[-1].isalpha():
            word_lower = word_lower[:-1]
        new_words_set.remove(word)
        new_words_set.add(word_lower)
    return new_words_set

story_senses = []
# [{},{}]
# [{dog: most_probable_sense, horse: sense}, {cat: sense}]

for story in input.story_sentences:
    for sentence in input.story_sentences[story]:
        sentence_senses = {}
        sentence_words = sentence.split()
        # set of words in the sentence
        words_set = remove_stopwords(set(sentence_words))
        # loop through all the words in the sentence to find their best senses
        for word in words_set:
            if word == "":
                continue
            word = word.lower()
            if not word[-1].isalpha():
                word = word[:-1]
            # all possible senses of the word
            all_senses = wn.synsets(word)
            # continue if there aren't any senses
            if len(all_senses) == 0:
                continue
            best_sense = ""
            max_overlap = 0
            # loop through all the senses
            for each_sense in all_senses:
                # set of words in the definition and examples
                signature_set = remove_stopwords(set(each_sense.definition().split()))
                for each_example in each_sense.examples():
                    signature_set.update(each_example.split())
                current_overlap = len(words_set.intersection(signature_set))
                if current_overlap >= max_overlap:
                    max_overlap = current_overlap
                    best_sense = each_sense
            sentence_senses[word] = best_sense
        story_senses.append(sentence_senses)

question_senses = {}
for story_id in input.question_data:
    story_questions = []
    all_questions = input.question_data[story_id]
    for question_id in all_questions:
        temp = all_questions[question_id]
        question_word_senses = {}
        question = all_questions[question_id][0]
        question_words_set = remove_stopwords(set(question.split()))
        for word in question_words_set:
            if word == "":
                continue
            if not word[-1].isalpha():
                word = word[:-1]
            word = word.lower()
            all_senses = wn.synsets(word)
            if len(all_senses) == 0:
                continue
            best_sense = ""
            max_overlap = 0
            # loop through all the senses
            for each_sense in all_senses:
                # set of words in the definition and examples
                signature_set = remove_stopwords(set(each_sense.definition().split()))
                for each_example in each_sense.examples():
                    signature_set.update(each_example.split())
                current_overlap = len(words_set.intersection(signature_set))
                if current_overlap >= max_overlap:
                    max_overlap = current_overlap
                    best_sense = each_sense
            question_word_senses[word] = best_sense
        story_questions.append(question_word_senses)
    question_senses[story_id] = story_questions


# print(question_senses)
# print(story_senses)



