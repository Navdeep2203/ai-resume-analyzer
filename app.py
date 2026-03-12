import streamlit as st
import spacy
import pandas as pd
import re
from PyPDF2 import PdfReader
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Skill database
SKILLS_DB = [
"python","java","c++","c","sql","machine learning","deep learning","nlp",
"pandas","numpy","tensorflow","pytorch","opencv","docker","aws","kubernetes",
"html","css","javascript","react","data analysis","flask","streamlit","mysql"
]

# Extract text from PDF
def extract_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


# Extract skills using NLP
def extract_skills(text):

    text = text.lower()

    doc = nlp(text)

    skills = []

    for token in doc:

        if token.text in SKILLS_DB:

            skills.append(token.text)

    return list(set(skills))


# Skill match score
def skill_match_score(resume_skills, required_skills):

    if len(required_skills) == 0:
        return 0, []

    matched = list(set(resume_skills) & set(required_skills))

    score = (len(matched) / len(required_skills)) * 100

    return round(score,2), matched


# Detect experience
def detect_experience(text):

    exp = re.findall(r'\d+\s+years?', text.lower())

    return exp


# Rank resumes
def rank_resumes(files, prompt):

    ranking = []

    prompt_skills = extract_skills(prompt)

    for file in files:

        text = extract_text(file)

        resume_skills = extract_skills(text)

        score, matched = skill_match_score(resume_skills, prompt_skills)

        ranking.append((file.name, score))

    ranking.sort(key=lambda x: x[1], reverse=True)

    return ranking


# ---------------- STREAMLIT UI ----------------

st.title("AI Resume Analyzer & Candidate Ranking System")

st.write("Upload resumes and compare them with job requirements.")

uploaded_files = st.file_uploader(
"Upload Resumes (PDF)", 
type=["pdf"], 
accept_multiple_files=True
)

prompt = st.text_area(
"Enter required skills / job description",
"Looking for a developer skilled in Python, SQL, Machine Learning and Docker"
)


if uploaded_files:

    prompt_skills = extract_skills(prompt)

    st.header("Required Skills")

    st.write(prompt_skills)

    ranking = []

    for file in uploaded_files:

        resume_text = extract_text(file)

        resume_skills = extract_skills(resume_text)

        match_score, matching = skill_match_score(resume_skills, prompt_skills)

        missing = list(set(prompt_skills) - set(resume_skills))

        ats_score = match_score

        if len(resume_skills) < 5:
            ats_score -= 10

        ranking.append((file.name, match_score))

        st.subheader(file.name)

        st.write("Match Score:", match_score,"%")

        st.write("ATS Score:", ats_score,"%")

        st.write("Detected Skills:", resume_skills)

        st.write("Matching Skills:", matching)

        st.write("Missing Skills:", missing)

        experience = detect_experience(resume_text)

        st.write("Detected Experience:", experience)

        # Skill frequency chart
        skill_freq = Counter(resume_skills)

        df = pd.DataFrame(skill_freq.items(), columns=["Skill","Count"])

        if not df.empty:

            st.bar_chart(df.set_index("Skill"))

        # Keyword extraction
        vectorizer = CountVectorizer(stop_words="english", max_features=10)

        X = vectorizer.fit_transform([resume_text])

        keywords = vectorizer.get_feature_names_out()

        st.write("Top Keywords:", keywords)

        # Word cloud
        wc = WordCloud(width=800,height=400).generate(resume_text)

        fig, ax = plt.subplots()

        ax.imshow(wc)

        ax.axis("off")

        st.pyplot(fig)

        # Suggestions
        st.write("Suggestions:")

        if "docker" not in resume_skills:
            st.write("• Add Docker experience")

        if "aws" not in resume_skills:
            st.write("• Cloud technologies like AWS improve resumes")

        if "machine learning" not in resume_skills:
            st.write("• Add ML related projects")

        st.write("---")


    # Candidate Ranking
    ranking.sort(key=lambda x: x[1], reverse=True)

    st.header("Candidate Ranking")

    for i, (name, score) in enumerate(ranking, start=1):

        st.write(f"{i}. {name} — {score}%")