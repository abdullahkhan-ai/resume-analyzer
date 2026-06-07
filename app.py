import streamlit as st
import pytesseract
from PIL import Image
from pypdf import PdfReader

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

        # -------------------
        # Extracted Text
        # -------------------

        with st.expander("🔍 View Extracted Resume Text"):

            st.text(resume_text[:5000])