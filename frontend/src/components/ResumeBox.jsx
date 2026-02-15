export default function ResumeBox({
  resumeText,
  setResumeText,
  resumeFile,
  setResumeFile,
}) {
  function handleResumePdf(e) {
    const selected = e.target.files?.[0];
    if (!selected) return;

    if (selected.type !== "application/pdf") {
      alert("Only PDF files are allowed for Resume.");
      return;
    }

    setResumeFile(selected);
  }

  function clearResumePdf() {
    setResumeFile(null);
  }

  return (
    <div className="card">
      <h3 className="cardTitle">Resume</h3>

      <p className="muted">Paste resume text OR upload a resume PDF.</p>

      <textarea
        className="textarea"
        placeholder="Paste resume text here..."
        value={resumeText}
        onChange={(e) => setResumeText(e.target.value)}
        disabled={!!resumeFile}
      />

      <div className="jdUpload">
        <input
          type="file"
          accept=".pdf"
          onChange={handleResumePdf}
          disabled={!!resumeText.trim()}
        />

        {resumeFile ? (
          <div className="jdFileRow">
            <span className="muted">
              Resume PDF: <b>{resumeFile.name}</b>
            </span>
            <button className="btn secondary" onClick={clearResumePdf}>
              Remove
            </button>
          </div>
        ) : (
          <p className="muted small">
            If resume text is pasted, upload will be disabled.
          </p>
        )}
      </div>
    </div>
  );
}