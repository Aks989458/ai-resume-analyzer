import { useState } from "react";
import { analyzeResume } from "./analyzerApi";

import Header from "./components/Header";
import JobDescription from "./components/JobDescription";
import AnalyzeButton from "./components/AnalyzeButton";
import ScoreCards from "./components/ScoreCards";
import SkillsList from "./components/SkillsList";
import RolePrediction from "./components/RolePredictions";
import Loader from "./components/Loader";
import ResumeBox from "./components/ResumeBox";

export default function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState("");

  const [jobDescription, setJobDescription] = useState("");
  const [jdFile, setJdFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleAnalyze() {
    setError("");
    setResult(null);

    // Resume must exist (text or pdf)
    if (!resumeText.trim() && !resumeFile) {
      setError("Please paste resume text OR upload resume PDF.");
      return;
    }

    // JD must exist (text or pdf)
    if (!jobDescription.trim() && !jdFile) {
      setError("Please paste job description OR upload JD PDF.");
      return;
    }

    try {
      setLoading(true);

      const data = await analyzeResume({
        resumeText,
        jdText: jobDescription,
        resumeFile,
        jdFile,
      });

      if (data?.error) {
        setError(data.error);
        return;
      }

      setResult(data);
    } catch (err) {
      console.error(err);
      setError(
        err?.response?.data?.detail ||
        "Failed to analyze resume. Check backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setResumeFile(null);
    setResumeText("");
    setJobDescription("");
    setJdFile(null);
    setResult(null);
    setError("");
  }

  return (
    <div className="app">
      <Header />

      <main className="container">
        <section className="panel">
          <h2 className="title">Analyze Resume vs Job Description</h2>

          <div className="grid">
            <ResumeBox
              resumeText={resumeText}
              setResumeText={setResumeText}
              resumeFile={resumeFile}
              setResumeFile={setResumeFile}
            />

            <JobDescription
              jobDescription={jobDescription}
              setJobDescription={setJobDescription}
              jdFile={jdFile}
              setJdFile={setJdFile}
            />
          </div>

          <div className="actions">
            <AnalyzeButton loading={loading} onClick={handleAnalyze} />
            <button className="btn secondary" onClick={handleReset}>
              Reset
            </button>
          </div>

          {error && <div className="error">{error}</div>}
        </section>

        {loading && (
          <section className="panel">
            <Loader />
          </section>
        )}

        {result && (
          <section className="panel">
            <h2 className="title">Results</h2>

            <ScoreCards result={result} />

            <div className="grid resultsGrid">
              <SkillsList
                title="Resume Skills"
                subtitle={`${result.resume_skills.length} skills detected`}
                skills={result.resume_skills}
              />
              <SkillsList
                title="JD Skills"
                subtitle={`${result.jd_skills.length} skills detected`}
                skills={result.jd_skills}
              />
              <SkillsList
                title="Missing Skills"
                subtitle={`${result.missing_skills.length} skills missing`}
                skills={result.missing_skills}
                variant="missing"
              />
              <RolePrediction rolePrediction={result.role_prediction} />
            </div>
          </section>
        )}
      </main>
    </div>
  );
}