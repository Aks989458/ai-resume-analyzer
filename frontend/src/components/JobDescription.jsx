export default function JobDescription({
  jobDescription,
  setJobDescription,
  jdFile,
  setJdFile,
}) {
  function handleJdPdf(e) {
    const selected = e.target.files?.[0];
    if (!selected) return;

    if (selected.type !== "application/pdf") {
      alert("Only PDF files are allowed for JD.");
      return;
    }

    setJdFile(selected);
  }

  function clearJdPdf() {
    setJdFile(null);
  }

  return (
    <div className="card">
      <h3 className="cardTitle">Job Description</h3>

      <p className="muted">
        Paste JD text OR upload a JD PDF (optional).
      </p>

      <textarea
        className="textarea"
        placeholder="Paste the job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        disabled={!!jdFile}
      />

      <div className="jdUpload">
        <input type="file" accept=".pdf" onChange={handleJdPdf} />

        {jdFile ? (
          <div className="jdFileRow">
            <span className="muted">
              JD PDF: <b>{jdFile.name}</b>
            </span>
            <button className="btn secondary" onClick={clearJdPdf}>
              Remove
            </button>
          </div>
        ) : (
          <p className="muted small">
            If JD PDF is uploaded, text input will be disabled.
          </p>
        )}
      </div>
    </div>
  );
}