export default function VeilleMarcheStepCard({ title, description, badgeLabel, badgeTone = "success" }) {
  return (
    <div className="table-card veille-marche-step-card">
      <div className="table-card__header">
        <div>
          <div className="table-card__title">{title}</div>
          {description && <p className="cell-muted">{description}</p>}
        </div>
        {badgeLabel && (
          <span className={`badge badge--${badgeTone}`}>{badgeLabel}</span>
        )}
      </div>
    </div>
  );
}
