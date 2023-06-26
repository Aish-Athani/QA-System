import spacy
import input

def get_answer_type(question):
    types = []
    tag = ""
    if "What team" in question:
        types.append("PERSON")
        types.append("ORG")
        tag = "NER"
    # elif "What movie" in question:
    #     types.append("PROPN")
    #     tag = "POS"
    elif "At what point" in question:
        types.append("TIME")
        types.append("QUANTITY")
        tag = "NER"
    elif "How often" in question:
        types.append("TIME")
        types.append("DATE")
        tag = "NER"
    elif "What" in question and "cost" in question:
        types.append("MONEY")
        tag = "NER"
    elif "What organization" in question:
        types.append("ORG")
        tag = "NER"
    # elif "What is the name" in question:
    #     types.append("ORG")
    #     types.append("PERSON")
    #     tag = "NER"
    elif "What" and "size" in question:
        types.append("CARDINAL")
        types.append("QUANTITY")
        tag = "NER"
    elif "What date" in question:
        types.append("DATE")
        tag = "NER"
    elif "What time" in question:
        types.append("TIME")
        tag = "NER"
    elif "What is the population" in question:
        types.append("CARDINAL")
        tag = "NER"
    # elif "At whose" in question or "at whose" in question:
    #     types.append("PERSON")
    #     tag = "NER"
    # elif "What" in question and "age" in question:
    #     types.append("CARDINAL")
    #     tag = "NER"
    elif "What birthday" in question:
        types.append("DATE")
        types.append("CARDINAL")
        tag = "NER"
    return types

def answer_trimming(question, answer):
    types = []
    if "What team" in question or "what team" in question:
        types = ["PERSON, ORG"]
    elif "At what point" in question:
        types = ["TIME", "QUANTITY"]
    elif "How often" in question:
        types = ["TIME", "DATE"]
    elif "What" in question and "cost" in question:
        types = ["MONEY"]
    elif "What organization" in question or "what organization" in question:
        types = ["ORG"]
    elif "What" and "size" in question:
        types = ["CARDINAL", "QUANTITY"]
    elif "What date" in question or "what date" in question:
        types = ["DATE"]
    elif "What time" in question or "what time" in question:
        types = ["TIME"]
    elif "What is the population" in question:
        types = ["CARDINAL"]
    elif "What birthday" in question:
        types = ["DATE", "CARDINAL"]
    return types
