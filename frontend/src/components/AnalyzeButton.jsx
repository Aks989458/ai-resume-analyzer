export default function AnalyzeButton({ loading, onClick }) {
  return (
    <button className="btn primary" onClick={onClick} disabled={loading}>
      {loading ? "Analyzing..." : "Analyze"}
    </button>
  );
}