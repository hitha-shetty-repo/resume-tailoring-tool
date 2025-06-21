import streamlit as st
import docx
import spacy
import os
import matplotlib.pyplot as plt
from utils import extract_text_from_docx, extract_skills_from_text, match_skills, categorize_skills, calculate_score

# 🔧 Auto-download spaCy model if missing
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="Resume Tailoring Tool", layout="wide")

st.title("📄 Resume Tailoring Tool")
st.markdown("Tailor your resume to any job description using AI 💼")

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("Upload your resume (.docx)", type=["docx"])
with col2:
    jd_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])

if resume_file and jd_file:
    resume_text = extract_text_from_docx(resume_file)
    jd_text = jd_file.read().decode("utf-8")

    st.subheader("🧠 Extracting & Matching Skills...")
    resume_skills = extract_skills_from_text(resume_text, nlp)
    jd_skills = extract_skills_from_text(jd_text, nlp)

    matched_skills, missing_skills = match_skills(resume_skills, jd_skills)
    hard_missing, soft_missing = categorize_skills(missing_skills)

    st.success(f"✅ Skills Matched: {len(matched_skills)} / {len(jd_skills)}")

    st.subheader("📊 Skill Match Summary")
    labels = 'Matched', 'Missing'
    sizes = [len(matched_skills), len(missing_skills)]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF5252'])
    ax.axis('equal')
    st.pyplot(fig)

    score = calculate_score(len(matched_skills), len(jd_skills), resume_text, matched_skills)

    st.metric("💯 Resume Match Score", f"{score}/100")

    st.subheader("🔍 Missing Skills Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.error("**Hard Skills**")
        st.write(hard_missing if hard_missing else "✅ None!")
    with col2:
        st.warning("**Soft Skills**")
        st.write(soft_missing if soft_missing else "✅ None!")

    st.subheader("📄 Tailored Resume Preview")
    st.code(resume_text, language='markdown')
