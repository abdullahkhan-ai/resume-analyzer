import streamlit as st
import pytesseract
from PIL import Image
from pypdf import PdfReader

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "png", "jpg", "jpeg"]
)


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
            st.error("Unable to read PDF.")

    else:
        try:
            image = Image.open(file)
            text = pytesseract.image_to_string(image)

        except Exception:
            st.error("Unable to read image.")

    return text


def analyze_resume(text):
    text = text.lower()

    score = 0
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

    detected_skills = []

    for skill in skills:
        if skill in text:
            detected_skills.append(skill.title())
            score += 10

    if "project" in text:
        score += 10
    else:
        feedback.append("Add a Projects section.")

    if "education" in text:
        score += 10
    else:
        feedback.append("Add an Education section.")

    if "experience" in text:
        score += 10
    else:
        feedback.append("Add an Experience section.")

    score = min(score, 100)

    return score, detected_skills, feedback


if uploaded_file:

    if st.button("Analyze Resume"):

        resume_text = extract_text(uploaded_file)

        score, skills, feedback = analyze_resume(resume_text)

        st.subheader("📊 Resume Score")
        st.progress(score / 100)
        st.success(f"{score}/100")

        st.subheader("📝 Resume Summary")

        if score >= 80:
            st.write(
                "Strong resume with relevant technical skills and good structure."
            )

        elif score >= 60:
            st.write(
                "Decent resume. Adding more projects, experience, and technical skills would improve it."
            )

        else:
            st.write(
                "Resume needs significant improvement in skills, projects, and structure."
            )

        st.subheader("💻 Skills Detected")

        if skills:
            for skill in skills:
                st.write(f"✅ {skill}")
        else:
            st.warning("No major skills detected.")

        st.subheader("📌 Suggestions")

        if feedback:
            for item in feedback:
                st.write(f"⚠️ {item}")
        else:
            st.success("Excellent Resume Structure!")

        with st.expander("View Extracted Resume Text"):
            st.text(resume_text[:5000])