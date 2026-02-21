export default function RolePrediction({ result }) {
  const ml = result?.ml_role_prediction;

  if (!ml) {
    return (
      <div className="card">
        <h3 className="cardTitle">Role Prediction</h3>
        <p className="muted">No role prediction available.</p>
      </div>
    );
  }

  const predicted = ml.predicted_role;
  const topRoles = ml.top_roles || [];

  return (
    <div className="card">
      <h3 className="cardTitle">ML Role Prediction</h3>

      <p className="muted">
        Predicted role: <b>{predicted}</b>
      </p>

      <div className="roleList">
        {topRoles.map((item) => (
          <div key={item.role} className="roleRow">
            <span className="roleName">{item.role}</span>
            <span className="roleScore">{item.confidence}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}