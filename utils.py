import docx
import json
from io import BytesIO
from docx import Document
import matplotlib.pyplot as plt

def extract_resume_text(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_keywords_spacy(text):
    return list(set([token.lemma_.lower() for token in text.split() if len(token) > 3]))

def match_keywords(resume_text, jd_keywords):
    resume_words = resume_text.lower()
    matched = [word for word in jd_keywords if word in resume_words]
    missing = [word for word in jd_keywords if word not in resume_words]
    return matched, missing

def categorize_skills(missing_skills):
    with open("data/skills.json", "r") as f:
        skill_data = json.load(f)
    hard = [skill for skill in missing_skills if skill in skill_data.get("hard", [])]
    soft = [skill for skill in missing_skills if skill in skill_data.get("soft", [])]
    return hard, soft

def get_relevant_sentences(resume_text, matched_skills):
    lines = resume_text.split("\n")
    return [line for line in lines if any(skill in line.lower() for skill in matched_skills)]

def calculate_resume_score(matched, total_keywords, relevant_sentences, total_lines, hard, soft):
    if total_keywords == 0:
        return 0
    match_ratio = len(matched) / total_keywords
    relevance_ratio = len(relevant_sentences) / max(total_lines, 1)
    penalty = 0.05 * len(hard) + 0.03 * len(soft)
    raw_score = (0.6 * match_ratio + 0.4 * relevance_ratio) * 100
    return round(max(raw_score - penalty * 100, 0), 2)

def create_tailored_resume(sentences):
    doc = Document()
    doc.add_heading("Tailored Resume", 0)
    for sentence in sentences:
        doc.add_paragraph(sentence)
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output

def draw_pie_chart(matched, missing):
    labels = 'Matched', 'Missing'
    sizes = [matched, missing]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF5252'])
    ax.axis('equal')
    return fig
