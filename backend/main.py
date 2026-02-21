from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from services.analyzer_phase1 import extract_text_from_pdf, analyze_resume_phase1

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SKILLS_CSV_PATH = "data/skills.csv"
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.delete("/clear-uploads")
def clear_uploads():
    upload_dir = "uploads"

    if os.path.exists(upload_dir):
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                return {"error": str(e)}

    return {"message": "Uploads cleared successfully"}

@app.post("/analyze")
async def analyze(
    resume_text: str = Form(""),
    job_description: str = Form(""),
    resume_file: UploadFile = File(None),
    jd_file: UploadFile = File(None),
):
    # -------------------------
    # Resume text handling
    # -------------------------
    final_resume_text = resume_text.strip()

    if not final_resume_text and resume_file:
        resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)
        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume_file.file, buffer)

        final_resume_text = extract_text_from_pdf(resume_path)

    # -------------------------
    # JD text handling
    # -------------------------
    final_jd_text = job_description.strip()

    if not final_jd_text and jd_file:
        jd_path = os.path.join(UPLOAD_DIR, jd_file.filename)
        with open(jd_path, "wb") as buffer:
            shutil.copyfileobj(jd_file.file, buffer)

        final_jd_text = extract_text_from_pdf(jd_path)

    # -------------------------
    # Validation
    # -------------------------
    if not final_resume_text:
        return {"error": "Please paste resume text OR upload resume PDF."}

    if not final_jd_text:
        return {"error": "Please paste job description OR upload JD PDF."}

    # -------------------------
    # Analyze
    # -------------------------
    result = analyze_resume_phase1(final_resume_text, final_jd_text, SKILLS_CSV_PATH)
    return result