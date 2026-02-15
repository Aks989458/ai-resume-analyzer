export default function RolePrediction({ rolePrediction }) {
  const predicted = rolePrediction?.predicted_role;
  const scores = rolePrediction?.role_scores || {};

  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const top = sorted.slice(0, 5);

  return (
    <div className="card">
      <h3 className="cardTitle">Role Prediction</h3>

      <p className="muted">
        Predicted role: <b>{predicted}</b>
      </p>

      <div className="roleList">
        {top.map(([role, score]) => (
          <div key={role} className="roleRow">
            <span className="roleName">{role}</span>
            <span className="roleScore">{score}%</span>
          </div>
        ))}
      </div>

      <p className="muted small">
        Tip: In Phase 2, we’ll replace this with a trained ML classifier.
      </p>
    </div>
  );
}