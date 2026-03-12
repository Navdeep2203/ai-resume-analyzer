import spacy

nlp = spacy.load("en_core_web_sm")

with open("skills.txt","r") as f:
    SKILLS = [skill.strip().lower() for skill in f.readlines()]

def extract_skills(text):

    doc = nlp(text.lower())

    detected_skills = []

    for token in doc:
        if token.text in SKILLS:
            detected_skills.append(token.text)

    return list(set(detected_skills))