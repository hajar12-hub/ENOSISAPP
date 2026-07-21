export default function VeilleMarcheSegmentChip({ label, active, onClick }) {
  return (
    <button
      type="button"
      className={`veille-marche-segment-chip${active ? " is-active" : ""}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
}
