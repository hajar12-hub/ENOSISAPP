export default function VeilleMarcheSelectionItem({ title, subtitle, onSelect, disabled }) {
  return (
    <div className="veille-marche-selection-item">
      <div>
        <div className="cell-strong">{title}</div>
        {subtitle && <div className="cell-muted">{subtitle}</div>}
      </div>
      <button
        type="button"
        className="button button--primary button--sm"
        onClick={onSelect}
        disabled={disabled}
      >
        Choisir
      </button>
    </div>
  );
}
