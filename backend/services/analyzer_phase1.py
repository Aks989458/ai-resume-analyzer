import re
import pandas as pd
import fitz

from services.ml_role_model import MLRoleClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------
# Load ML model once (global, but safe)
# ---------------------------------------------------
ml_model = MLRoleClassifier()


# ---------------------------------------------------
# 1) Extract text from PDF
# ---------------------------------------------------
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return "\n".join(pages)


# ---------------------------------------------------
# 2) Clean text
# ---------------------------------------------------
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------------------------------------------
# 3) TF-IDF + Cosine similarity
# ---------------------------------------------------
def compute_text_similarity(resume_text: str, jd_text: str) -> float:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(sim)


# ---------------------------------------------------
# 4) Load skills list from CSV
# ---------------------------------------------------
def load_skills(skills_csv_path: str) -> list[str]:
    df = pd.read_csv(skills_csv_path)
    skills = df["skill"].dropna().astype(str).str.lower().tolist()
    return sorted(list(set(skills)))


# ---------------------------------------------------
# 5) Extract skills using regex
# ---------------------------------------------------
def extract_skills(text: str, skills_list: list[str]) -> list[str]:
    found = []
    for skill in skills_list:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found.append(skill)
    return sorted(list(set(found)))


# ---------------------------------------------------
# 6) Skill overlap score
# ---------------------------------------------------
def skill_overlap_score(resume_skills: list[str], jd_skills: list[str]) -> float:
    jd_set = set(jd_skills)
    if len(jd_set) == 0:
        return 0.0

    overlap = len(set(resume_skills).intersection(jd_set))
    return float(overlap / len(jd_set))


# ---------------------------------------------------
# 7) Final weighted score
# ---------------------------------------------------
def final_match_score(text_sim: float, skill_sim: float) -> float:
    return float(0.6 * text_sim + 0.4 * skill_sim)


# ---------------------------------------------------
# 8) Rule-based role prediction (kept for comparison)
# ---------------------------------------------------
ROLE_SKILL_MAP = {
    "Frontend Developer": [
        "html", "css", "javascript", "typescript", "react", "nextjs",
        "tailwind", "redux", "responsive design", "ui/ux"
    ],
    "Backend Developer": [
        "nodejs", "express", "fastapi", "flask", "django",
        "rest api", "sql", "mongodb", "postgresql", "docker"
    ],
    "Machine Learning Engineer": [
        "python", "numpy", "pandas", "scikit-learn",
        "machine learning", "mlflow", "model deployment"
    ],
    "DevOps Engineer": [
        "linux", "docker", "kubernetes", "aws", "azure", "gcp"
    ],
}


def predict_role_rule_based(resume_skills: list[str]):
    resume_set = set(resume_skills)

    scores = {}
    for role, required_skills in ROLE_SKILL_MAP.items():
        required_set = set(required_skills)

        matched = len(resume_set.intersection(required_set))
        total = len(required_set)

        score = matched / total if total != 0 else 0
        scores[role] = score

    best_role = max(scores, key=scores.get)

    return {
        "predicted_role": best_role,
        "role_scores": {k: round(v * 100, 2) for k, v in scores.items()}
    }


# ---------------------------------------------------
# 9) MAIN ANALYSIS FUNCTION
# ---------------------------------------------------
def analyze_resume_phase1(resume_text: str, jd_text: str, skills_csv_path: str):

    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    skills_list = load_skills(skills_csv_path)

    # Similarity
    text_sim = compute_text_similarity(resume_text, jd_text)

    # Skills extraction
    resume_skills = extract_skills(resume_text, skills_list)
    jd_skills = extract_skills(jd_text, skills_list)

    missing_skills = sorted(list(set(jd_skills) - set(resume_skills)))

    skill_sim = skill_overlap_score(resume_skills, jd_skills)

    final_score = final_match_score(text_sim, skill_sim)

    # Rule-based role prediction
    rule_role_pred = predict_role_rule_based(resume_skills)

    # ML-based role prediction (NEW)
    ml_role_prediction = ml_model.predict(resume_text)

    return {
        "text_similarity": round(text_sim * 100, 2),
        "skill_similarity": round(skill_sim * 100, 2),
        "final_score": round(final_score * 100, 2),
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "missing_skills": missing_skills,
        "rule_based_role_prediction": rule_role_pred,
        "ml_role_prediction": ml_role_prediction
    }