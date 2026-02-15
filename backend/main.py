from fastapi import FastAPI, UploadFile, File, Form
import os
import shutil

from services.analyzer_phase1 import extract_text_from_pdf, analyze_resume_phase1

app = FastAPI()

SKILLS_CSV_PATH = "data/skills.csv"
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), job_description: str = Form(...)):
    pdf_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text_from_pdf(pdf_path)

    result = analyze_resume_phase1(resume_text, job_description, SKILLS_CSV_PATH)

    return result