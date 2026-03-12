# AI Resume Analyzer & Candidate Ranking System

An NLP-based web application that analyzes resumes and compares them with job requirements.

## Features

- Resume upload (multiple PDFs)
- Skill extraction using NLP (spaCy)
- Skill-based match score
- ATS-style resume scoring
- Candidate ranking system
- Keyword extraction
- Resume word cloud visualization
- Resume improvement suggestions

## Tech Stack

Python  
Streamlit  
spaCy NLP  
Scikit-learn  
PyPDF2  

## How It Works

1. Upload resumes
2. Enter required skills or job description
3. The system extracts skills from resumes using NLP
4. Skills are compared with job requirements
5. Match score and ATS score are calculated
6. Candidates are ranked automatically

## Run the Project

Install dependencies

```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Run the app

```
streamlit run app.py
```

## Example

Prompt:

```
Looking for Python, SQL, Machine Learning, Docker
```

Output:

```
Resume1.pdf → 75%
Resume2.pdf → 63%
Resume3.pdf → 41%
```

Candidates are ranked automatically.
