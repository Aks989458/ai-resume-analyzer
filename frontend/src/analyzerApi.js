import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export async function analyzeResume({
  resumeText,
  jdText,
  resumeFile,
  jdFile,
}) {
  const formData = new FormData();

  formData.append("resume_text", resumeText || "");
  formData.append("job_description", jdText || "");

  if (resumeFile) formData.append("resume_file", resumeFile);
  if (jdFile) formData.append("jd_file", jdFile);

  const res = await axios.post(`${API_BASE}/analyze`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data;
}