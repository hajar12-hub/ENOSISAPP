export default function VeilleMarcheSummaryField({ label, value }) {
  return (
    <div className="meta-field">
      <span className="meta-field__label">{label}</span>
      <span className="meta-field__value">{value ?? "—"}</span>
    </div>
  );
}
