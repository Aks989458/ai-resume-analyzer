function ScoreCard({ label, value }) {
  return (
    <div className="scoreCard">
      <p className="scoreLabel">{label}</p>
      <p className="scoreValue">{value}%</p>
    </div>
  );
}

export default function ScoreCards({ result }) {
  return (
    <div className="scoreRow">
      <ScoreCard label="Text Similarity" value={result.text_similarity} />
      <ScoreCard label="Skill Similarity" value={result.skill_similarity} />
      <ScoreCard label="Final Score" value={result.final_score} />
    </div>
  );
}