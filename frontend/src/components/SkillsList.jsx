export default function SkillsList({ title, subtitle, skills, variant }) {
  return (
    <div className="card">
      <h3 className="cardTitle">{title}</h3>
      <p className="muted">{subtitle}</p>

      <div className="chips">
        {skills.length === 0 ? (
          <p className="muted">No skills found</p>
        ) : (
          skills.map((s) => (
            <span
              key={s}
              className={`chip ${variant === "missing" ? "chipMissing" : ""}`}
            >
              {s}
            </span>
          ))
        )}
      </div>
    </div>
  );
}