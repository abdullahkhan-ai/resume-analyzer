import streamlit as st
import pytesseract
from PIL import Image
from pypdf import PdfReader
from reportlab.pdfgen import canvas

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet

import os
from textwrap import wrap
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

st.set_page_config(
    page_title="Resume Analyzer Pro",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Analyzer Pro V5")

# ---------------------------
# Job Role Selection
# ---------------------------

job_role = st.selectbox(
    "🎯 Select Target Role",
    [
        "AI Engineer",
        "Data Scientist",
        "Software Engineer"
    ]
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "png", "jpg", "jpeg"]
)


# ---------------------------
# Extract Resume Text
# ---------------------------

def extract_text(file):

    text = ""

    if file.name.lower().endswith(".pdf"):

        try:
            pdf = PdfReader(file)

            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text

        except Exception:
            st.error("Could not read PDF.")

    else:

        try:
            image = Image.open(file)
            text = pytesseract.image_to_string(image)

        except Exception:
            st.error("Could not read image.")

    return text


# ---------------------------
# Analyze Resume
# ---------------------------

def analyze_resume(resume_text):

    resume_lower = resume_text.lower()

    score = 0
    found_skills = []
    feedback = []

    skills = [
        "python",
        "machine learning",
        "streamlit",
        "sql",
        "pandas",
        "numpy",
        "git",
        "github"
    ]

    # Skill Detection

    for skill in skills:

        if skill in resume_lower:
            found_skills.append(skill.title())
            score += 10

    # Resume Sections

    if "project" in resume_lower:
        score += 10
    else:
        feedback.append("Add a Projects section.")

    if "education" in resume_lower:
        score += 10
    else:
        feedback.append("Add an Education section.")

    if "experience" in resume_lower:
        score += 10
    else:
        feedback.append("Add an Experience section.")

    score = min(score, 100)

    # -----------------------
    # Job Match Score
    # -----------------------

    if job_role == "AI Engineer":

        required_skills = [
            "python",
            "machine learning",
            "tensorflow",
            "pytorch"
        ]

    elif job_role == "Data Scientist":

        required_skills = [
            "python",
            "sql",
            "pandas",
            "numpy"
        ]

    else:

        required_skills = [
            "python",
            "git",
            "github",
            "sql"
        ]

    missing_skills = []

    for skill in required_skills:

        if skill not in resume_lower:
            missing_skills.append(skill.title())

    match_score = int(
        (
            (len(required_skills) - len(missing_skills))
            / len(required_skills)
        )
        * 100
    )

    return (
        score,
        found_skills,
        feedback,
        match_score,
        missing_skills
    )

def get_ai_feedback(resume_text, job_role):

    prompt = f"""
    You are an expert resume reviewer.

    Target Role:
    {job_role}

    Resume:
    {resume_text}

    Give:
    1. Strengths
    2. Weaknesses
    3. Missing Skills
    4. ATS Improvement Suggestions

    Keep the response concise.
    """

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Error: {e}"
def create_pdf_report(
    score,
    match_score,
    found_skills,
    missing_skills,
    ai_feedback
):

    pdf_file = "resume_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("Resume Analysis Report", styles["Title"])
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"<b>Resume Score:</b> {score}/100",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Job Match Score:</b> {match_score}%",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph("<b>Skills Detected</b>", styles["Heading2"])
    )

    if found_skills:

        for skill in found_skills:

            content.append(
                Paragraph(f"• {skill}", styles["Normal"])
            )

    else:

        content.append(
            Paragraph(
                "No skills detected.",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph("<b>Missing Skills</b>", styles["Heading2"])
    )

    if missing_skills:

        for skill in missing_skills:

            content.append(
                Paragraph(f"• {skill}", styles["Normal"])
            )

    else:

        content.append(
            Paragraph(
                "No missing skills detected.",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph("<b>AI Feedback</b>", styles["Heading2"])
    )

    clean_feedback = (
        ai_feedback
        .replace("**", "")
        .replace("#", "")
    )

    content.append(
        Paragraph(
            clean_feedback.replace("\n", "<br/>"),
            styles["Normal"]
        )
    )

    doc.build(content)

    return pdf_file


        
# ---------------------------
# Main App
# ---------------------------

if uploaded_file:

    if st.button("Analyze Resume"):

        resume_text = extract_text(uploaded_file)

        (
            score,
            found_skills,
            feedback,
            match_score,
            missing_skills
        ) = analyze_resume(resume_text)

        # -------------------
        # Dashboard
        # -------------------

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("📊 Resume Score", f"{score}/100")

        with col2:
            st.metric("🎯 Job Match", f"{match_score}%")

        st.subheader("📊 Resume Score")
        st.progress(score / 100)

        st.subheader("🎯 Job Match Score")
        st.progress(match_score / 100)

        # -------------------
        # Resume Summary
        # -------------------

        st.subheader("📝 Resume Summary")

        if score >= 80:

            st.success(
                "Strong resume with relevant technical skills and good structure."
            )

        elif score >= 60:

            st.warning(
                "Decent resume. Adding more projects and experience would improve it."
            )

        else:

            st.error(
                "Resume needs significant improvement in skills and structure."
            )

        # -------------------
        # Skills Detected
        # -------------------

        st.subheader("💻 Skills Detected")

        if found_skills:

            for skill in found_skills:
                st.write(f"✅ {skill}")

        else:

            st.warning("No major skills detected.")

        # -------------------
        # Missing Skills
        # -------------------

        st.subheader("🚀 Missing Skills")

        if missing_skills:

            for skill in missing_skills:
                st.write(f"❌ {skill}")

        else:

            st.success("All required skills found!")

        # -------------------
        # Suggestions
        # -------------------

        st.subheader("📌 Suggestions")

        if feedback:

            for item in feedback:
                st.write(f"⚠️ {item}")

        else:

            st.success("Excellent Resume Structure!")
            st.subheader("🤖 Gemini AI Feedback")

        with st.spinner("Analyzing resume with Gemini AI..."):

            ai_feedback = get_ai_feedback(
                resume_text,
                job_role
            )

        st.write(ai_feedback)

        pdf_file = create_pdf_report(
    score,
    match_score,
    found_skills,
    missing_skills,
    ai_feedback
)

        with open(pdf_file, "rb") as file:

            st.download_button(
        label="📄 Download PDF Report",
        data=file,
        file_name="Resume_Report.pdf",
        mime="application/pdf"
    )

            

        # -------------------
        # Extracted Text
        # -------------------

        with st.expander("🔍 View Extracted Resume Text"):

            st.text(resume_text[:5000])