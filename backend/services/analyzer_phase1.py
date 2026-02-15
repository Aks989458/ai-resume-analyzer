import re
import pandas as pd
import fitz 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#1 Extract text from pdf
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return "\n".join(pages)

#2 Clean text
def clean_text(text: str)-> str:
    text = text.lower() 
    text = re.sub(r"\s+"," ",text)
    return text.strip()

#3 TF-IDF + Cosine similarity
def compute_text_similarity(resume_text: str, jd_text: str) -> float:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    sim = cosine_similarity(tfidf_matrix[0:1],tfidf_matrix[1:2])[0][0]
    return float(sim)

#4 Load skills list from csv
def load_skills(skills_csv_path: str) -> list[str]:
    df = pd.read_csv(skills_csv_path)
    skills = df['skill'].dropna().astype(str).str.lower().tolist()
    return sorted(list(set(skills)))

#5 Extract skills using regex
def extract_skills(text: str, skills_list: list[str]) -> list[str]:
    found = []
    for skill in skills_list:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found.append(skill)
    return sorted(list(set(found)))


#6 Skill overlap score
def skill_overlap_score(resume_skills: list[str], jd_skills: list[str]) -> float:
    jd_set = set(jd_skills)
    if len(jd_set) == 0:
        return 0.0
    overlap = len(set(resume_skills).intersection(jd_set))
    return float(overlap / len(jd_set))

# 7) Final score
def final_match_score(text_sim: float, skill_sim: float) -> float:
    return float(0.6 * text_sim + 0.4 * skill_sim)


# 8) Rule-based role prediction
ROLE_SKILL_MAP = {
    "Frontend Developer": [
        "html", "css", "javascript", "typescript", "react", "nextjs",
        "tailwind", "redux", "redux toolkit", "react router",
        "responsive design", "ui/ux", "dom", "axios",
        "jest", "react testing library", "cypress", "vite"
    ],

    "Backend Developer": [
        "nodejs", "express", "fastapi", "flask", "django",
        "rest api", "graphql", "jwt", "authentication",
        "authorization", "sql", "postgresql", "mongodb",
        "redis", "microservices", "nginx", "docker"
    ],

    "Full Stack Developer": [
        "react", "nextjs", "nodejs", "express", "rest api",
        "sql", "postgresql", "mongodb", "docker",
        "authentication", "jwt", "git", "github"
    ],

    "Data Analyst": [
        "sql", "excel", "power bi", "tableau",
        "data analysis", "statistics", "eda",
        "data cleaning", "matplotlib", "plotly"
    ],

    "Data Engineer": [
        "sql", "etl", "data pipelines", "airflow", "dbt",
        "spark", "hadoop", "big data", "data warehousing",
        "aws", "gcp", "azure"
    ],

    "Machine Learning Engineer": [
        "python", "numpy", "pandas", "scikit-learn",
        "machine learning", "model training", "model evaluation",
        "feature engineering", "hyperparameter tuning",
        "xgboost", "mlops", "mlflow", "model deployment",
        "fastapi", "docker"
    ],

    "NLP Engineer": [
        "python", "nlp", "spacy", "nltk", "transformers",
        "bert", "llm", "tokenization", "named entity recognition",
        "sentiment analysis", "rag", "vector database"
    ],

    "Computer Vision Engineer": [
        "python", "opencv", "computer vision", "image processing",
        "cnn", "object detection", "yolo", "face detection",
        "pose estimation", "ocr"
    ],

    "DevOps Engineer": [
        "linux", "docker", "kubernetes", "aws", "azure", "gcp",
        "ci/cd", "github actions", "jenkins",
        "terraform", "nginx", "monitoring",
        "prometheus", "grafana"
    ]
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

#9 Main function 
def analyze_resume_phase1(resume_text: str,jd_text: str, skills_csv_path: str):
    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    skills_list = load_skills(skills_csv_path)

    text_sim = compute_text_similarity(resume_text, jd_text)
    resume_skills = extract_skills(resume_text, skills_list)
    jd_skills = extract_skills(jd_text, skills_list)    

    missing_skills = sorted(list(set(jd_skills) - set(resume_skills)))

    skill_sim = skill_overlap_score(resume_skills,jd_skills)

    final_score = final_match_score(text_sim, skill_sim)

    role_pred = predict_role_rule_based(resume_skills)


    return {
        "text_similarity": round(text_sim * 100, 2),
        "skill_similarity": round(skill_sim * 100, 2),
        "final_score": round(final_score * 100, 2),
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "missing_skills": missing_skills,
        "role_prediction": role_pred
    }