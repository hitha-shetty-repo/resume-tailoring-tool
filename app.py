
import streamlit as st
from utils import *
import base64

st.set_page_config(page_title="Resume Tailoring Tool", layout="wide")
st.title("📄 Resume Tailoring Tool")

st.markdown("""
Upload your **resume** and **job description**, and this app will:
- Extract keywords from the JD
- Highlight matching and missing skills
- Categorize missing skills (Hard vs Soft)
- Display skill match pie chart
- Show a final Resume Match Score
- Generate a tailored resume (downloadable)
""")

resume_file = st.file_uploader("📤 Upload Resume (.docx)", type=["docx"])
jd_file = st.file_uploader("📄 Upload Job Description (.txt)", type=["txt"])

if resume_file and jd_file:
    resume_text = extract_resume_text(resume_file)
    jd_text = jd_file.read().decode("utf-8")

    with st.expander("🔍 Step 1: Extracted JD Keywords"):
        jd_keywords = extract_keywords_spacy(jd_text)
        st.write(jd_keywords)

    with st.expander("📋 Step 2: Skill Matching"):
        matched, missing = match_keywords(resume_text, jd_keywords)
        st.success(f"Matched: {len(matched)}")
        st.error(f"Missing: {len(missing)}")
        st.write("✅ Matched:", matched)
        st.write("❌ Missing:", missing)

    with st.expander("🧠 Step 3: Skill Categorization"):
        hard, soft = categorize_skills(missing)
        st.write("🛠 Hard Skills:", hard)
        st.write("🤝 Soft Skills:", soft)

    with st.expander("📊 Step 4: Skill Match Chart"):
        st.pyplot(draw_pie_chart(len(matched), len(missing)))

    with st.expander("✨ Step 5: Relevant Resume Sentences"):
        relevant_sentences = get_relevant_sentences(resume_text, matched)
        st.write(relevant_sentences)

    with st.expander("📈 Step 6: Resume Match Score"):
        score = calculate_resume_score(matched, len(jd_keywords), relevant_sentences, len(resume_text.split('\n')), hard, soft)
        st.metric(label="📈 Match Score", value=f"{score}%")
        st.markdown("### 📊 Score Breakdown")
        st.write({
            "Skill Match": f"{len(matched)}/{len(jd_keywords)}",
            "Relevant Sentences": f"{len(relevant_sentences)} lines",
            "Hard Skills Missing": len(hard),
            "Soft Skills Missing": len(soft),
            "Score": f"{score}%"
        })

    with st.expander("📄 Step 7: Download Tailored Resume"):
        tailored_doc = create_tailored_resume(relevant_sentences)
        st.download_button("📥 Download Tailored Resume", tailored_doc.getvalue(), file_name="Tailored_Resume.docx")
