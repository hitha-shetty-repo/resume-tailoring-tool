import streamlit as st
import matplotlib.pyplot as plt
import spacy
import en_core_web_sm
from utils import (
    extract_resume_text,
    extract_keywords_spacy,
    match_keywords,
    categorize_skills,
    get_relevant_sentences,
    create_tailored_resume,
    calculate_resume_score,
    draw_pie_chart
)

nlp = en_core_web_sm.load()

st.set_page_config(page_title="Resume Tailoring Tool", layout="wide")
st.title("📄 Resume Tailoring Tool")

st.markdown("""
Upload your **resume** and **job description**, and this app will:
- Extract keywords from the JD
- Highlight matching and missing skills
- Categorize missing skills (Hard vs Soft)
- Display a skill match pie chart
- Show a final Resume Match Score
- Generate a tailored resume (downloadable)
""")

resume_file = st.file_uploader("Upload Resume (.docx)", type=["docx"])
jd_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])

if resume_file and jd_file:
    resume_text = extract_resume_text(resume_file)
    jd_text = jd_file.read().decode("utf-8")

    jd_keywords = extract_keywords_spacy(jd_text)
    matched, missing = match_keywords(resume_text, jd_keywords)
    hard, soft = categorize_skills(missing)
    relevant_sentences = get_relevant_sentences(resume_text, matched)
    score = calculate_resume_score(matched, len(jd_keywords), relevant_sentences, len(resume_text.split("\n")), hard, soft)

    st.subheader("📊 Skill Match Summary")
    st.pyplot(draw_pie_chart(len(matched), len(missing)))
    st.metric(label="💯 Resume Match Score", value=f"{score}%")

    st.write("✅ Matched Skills:", matched)
    st.write("❌ Missing Skills:", missing)
    st.write("🛠 Hard Skills:", hard)
    st.write("🤝 Soft Skills:", soft)

    st.subheader("📄 Tailored Resume Preview")
    st.write(relevant_sentences)

    tailored_doc = create_tailored_resume(relevant_sentences)
    st.download_button("📥 Download Tailored Resume", tailored_doc.getvalue(), file_name="Tailored_Resume.docx")
