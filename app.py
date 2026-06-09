import streamlit as st
from pypdf import PdfReader

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet

import os
from textwrap import wrap
import os
from textwrap import wrap
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")



st.set_page_config(
    page_title="Resume Analyzer Pro",
    page_icon="📄",
    layout="wide"
)
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #F5F7FA;
}

/* Main Title */
.main-title {
    text-align: center;
    color: #FFD700;
    font-size: 48px;
    font-weight: bold;
}

/* Subtitle */
.sub-title {
    text-align: center;
    color: white;
    font-size: 18px;
}

/* Header Box */
.header-box {
    background: linear-gradient(90deg, #0A3D91, #1E5CCB);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: white;
    border: 2px solid #FFD700;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}

/* Buttons */
.stButton button {
    background-color: #0A3D91;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #1E5CCB;
}

/* Download Button */
.stDownloadButton button {
    background-color: #FFD700;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="header-box">
    <div class="main-title"> Resume Analyzer Pro </div>
    <div class="sub-title">
        AI Powered Resume Intelligence Platform
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Job Role Selection
# ---------------------------

st.markdown("## 🎯 Target Role")
job_role = st.selectbox(
    "🎯 Select Target Role",
    [
        "AI Engineer",
        "Machine Learning Engineer",
        "Data Scientist",
        "Data Analyst",
        "Business Analyst",
        "Software Engineer",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "Python Developer",
        "Java Developer",
        "Cloud Engineer",
        "DevOps Engineer",
        "Cybersecurity Analyst",
        "Network Engineer",
        "Prompt Engineer",
        "AI Product Manager",
        "Quant Developer",
        "Quantitative Analyst",
        "Algorithmic Trader",
        "FinTech Engineer",
        "Blockchain Developer",
        "Mobile App Developer",
        "UI/UX Designer",
        "Product Manager"
    ]
)

st.markdown("## 📂 Upload Resume")
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
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

     st.error(
        "Only PDF resumes are supported in the deployed version."
    )

    return text


# ---------------------------
# Analyze Resume
# ---------------------------
JOB_REQUIREMENTS = {

    "AI Engineer": [
        "python", "machine learning", "tensorflow",
        "pytorch", "deep learning", "nlp"
    ],

    "Machine Learning Engineer": [
        "python", "machine learning", "tensorflow",
        "pytorch", "scikit-learn"
    ],

    "Data Scientist": [
        "python", "sql", "pandas",
        "numpy", "machine learning"
    ],

    "Data Analyst": [
        "sql", "excel", "power bi",
        "tableau", "python"
    ],

    "Business Analyst": [
        "excel", "power bi",
        "tableau", "sql"
    ],

    "Software Engineer": [
        "python", "git", "github",
        "sql", "oop"
    ],

    "Backend Developer": [
        "python", "django",
        "flask", "api", "sql"
    ],

    "Frontend Developer": [
        "html", "css",
        "javascript", "react"
    ],

    "Full Stack Developer": [
        "html", "css",
        "javascript", "react",
        "node", "sql"
    ],

    "Python Developer": [
        "python", "flask",
        "django", "sql"
    ],

    "Java Developer": [
        "java", "spring",
        "sql", "oop"
    ],

    "Cloud Engineer": [
        "aws", "azure",
        "gcp", "docker"
    ],

    "DevOps Engineer": [
        "docker", "kubernetes",
        "jenkins", "linux"
    ],

    "Cybersecurity Analyst": [
        "network security",
        "penetration testing",
        "siem",
        "linux"
    ],

    "Network Engineer": [
        "networking",
        "ccna",
        "routing",
        "switching"
    ],

    "Prompt Engineer": [
        "prompt engineering",
        "llm",
        "chatgpt",
        "gemini"
    ],

    "AI Product Manager": [
        "ai",
        "product management",
        "analytics"
    ],

    "Quant Developer": [
        "python",
        "statistics",
        "finance",
        "algorithms"
    ],

    "Quantitative Analyst": [
        "statistics",
        "probability",
        "python",
        "finance"
    ],

    "Algorithmic Trader": [
        "python",
        "trading",
        "finance",
        "backtesting"
    ],

    "FinTech Engineer": [
        "python",
        "finance",
        "api",
        "sql"
    ],

    "Blockchain Developer": [
        "solidity",
        "ethereum",
        "web3"
    ],

    "Mobile App Developer": [
        "android",
        "ios",
        "flutter",
        "react native"
    ],

    "UI/UX Designer": [
        "figma",
        "wireframe",
        "prototype",
        "design"
    ],

    "Product Manager": [
        "product management",
        "analytics",
        "agile"
    ]
}
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
        "github",
        "tensorflow",
        "pytorch",
        "docker",
        "aws",
        "azure",
        "react",
        "flask",
        "django"
    ]

    # -----------------------
    # Skills Score (20)
    # -----------------------

    skills_score = 0

    for skill in skills:

        if skill in resume_lower:

            found_skills.append(skill.title())

            skills_score += 2

    skills_score = min(skills_score, 20)

    score += skills_score

    # -----------------------
    # Projects Score (20)
    # -----------------------

    project_keywords = [
        "project",
        "developed",
        "built",
        "implemented",
        "created"
    ]

    project_score = 0

    for keyword in project_keywords:

        if keyword in resume_lower:

            project_score += 4

    project_score = min(project_score, 20)

    score += project_score

    # -----------------------
    # Experience Score (20)
    # -----------------------

    experience_keywords = [
        "intern",
        "internship",
        "freelance",
        "experience",
        "developer"
    ]

    experience_score = 0

    for keyword in experience_keywords:

        if keyword in resume_lower:

            experience_score += 4

    experience_score = min(experience_score, 20)

    score += experience_score

    # -----------------------
    # Education Score (15)
    # -----------------------

    education_keywords = [
        "btech",
        "be",
        "bachelor",
        "engineering",
        "university"
    ]

    education_score = 0

    for keyword in education_keywords:

        if keyword in resume_lower:

            education_score += 3

    education_score = min(education_score, 15)

    score += education_score

    # -----------------------
    # Certifications Score (10)
    # -----------------------

    cert_keywords = [
        "certification",
        "coursera",
        "udemy",
        "google",
        "aws"
    ]

    cert_score = 0

    for keyword in cert_keywords:

        if keyword in resume_lower:

            cert_score += 2

    cert_score = min(cert_score, 10)

    score += cert_score

    # -----------------------
    # GitHub / LinkedIn (10)
    # -----------------------

    if "github" in resume_lower:
        score += 5

    if "linkedin" in resume_lower:
        score += 5

    # -----------------------
    # Structure Score (5)
    # -----------------------

    if "project" not in resume_lower:
        feedback.append("Add a Projects section.")

    if "education" not in resume_lower:
        feedback.append("Add an Education section.")

    if "experience" not in resume_lower:
        feedback.append("Add an Experience section.")

    if (
        "project" in resume_lower
        and "education" in resume_lower
        and "experience" in resume_lower
    ):
        score += 5

    score = min(score, 100)

    # -----------------------
    # Job Match Score
    # -----------------------

    required_skills = JOB_REQUIREMENTS.get(
        job_role,
        []
    )

    matched_skills = 0

    for skill in required_skills:

        if skill.lower() in resume_lower:

            matched_skills += 1

            if skill.title() not in found_skills:

                found_skills.append(skill.title())

    missing_skills = []

    for skill in required_skills:

        if skill.lower() not in resume_lower:

            missing_skills.append(skill.title())

    skill_score = (
        matched_skills / len(required_skills)
    ) * 70

    project_score = 0

    project_keywords = [
        "project",
        "developed",
        "built",
        "implemented",
        "created"
    ]

    for keyword in project_keywords:

        if keyword in resume_lower:

            project_score += 6

    project_score = min(project_score, 30)

    match_score = int(
        skill_score + project_score
    )

    match_score = min(match_score, 100)

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

    except Exception:

        return """
⚠️ Gemini AI Feedback Temporarily Unavailable

Possible reasons:
• Gemini service unavailable

Please try again later.
"""
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

        ats_score = int((score + match_score) / 2)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="📊 Resume Score",
                value=f"{score}/100"
            )

        with col2:
            st.metric(
                label="🎯 Job Match",
                value=f"{match_score}%"
            )

        with col3:
            st.metric(
                label="🤖 ATS Score",
                value=f"{ats_score}/100"
            )

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

            skills_html = ""

            for skill in found_skills:

                skills_html += f"""
                <span style="
                background:#0A3D91;
                color:white;
                padding:8px 14px;
                border-radius:20px;
                margin:5px;
                display:inline-block;
                font-weight:bold;">
                {skill}
                </span>
                """

            st.markdown(
                skills_html,
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "No major skills detected."
            )

        # -------------------
        # Suggestions
        # -------------------

        st.subheader("📌 Suggestions")

        if feedback:

            for item in feedback:

                st.write(f"⚠️ {item}")

        else:

            st.success(
                "Excellent Resume Structure!"
            )

        # -------------------
        # Gemini AI Feedback
        # -------------------

        st.subheader("🤖 Gemini AI Feedback")

        with st.spinner(
            "Analyzing resume with Gemini AI..."
        ):

            ai_feedback = get_ai_feedback(
                resume_text,
                job_role
            )

        st.write(ai_feedback)

        # -------------------
        # PDF Download
        # -------------------

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

        with st.expander(
            "🔍 View Extracted Resume Text"
        ):

            st.text(
                resume_text[:5000]
            )