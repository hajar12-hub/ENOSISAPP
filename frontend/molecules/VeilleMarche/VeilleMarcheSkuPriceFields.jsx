import { validateSkuPrice } from "../../utils/veilleMarcheValidation";

export default function VeilleMarcheSkuPriceFields({ skuLabel, marqueNom, value, onChange }) {
  const errors = validateSkuPrice(value);

  const handleChange = (field) => (e) => {
    const raw = e.target.value;
    onChange({ ...value, [field]: raw === "" ? "" : Number(raw) });
  };

  return (
    <div className="veille-marche-sku-row">
      <div className="veille-marche-sku-row__label">
        <span className="cell-strong">{skuLabel}</span>
        <span className="cell-muted">{marqueNom}</span>
      </div>

      <div className="field-row">
        <div className="field-group">
          <label className="field-label">Prix conso TTC</label>
          <input
            type="number"
            step="0.01"
            min="0"
            inputMode="decimal"
            className={`input-base${errors.prix_conso_ttc ? " is-invalid" : ""}`}
            placeholder="0.00"
            value={value.prix_conso_ttc ?? ""}
            onChange={handleChange("prix_conso_ttc")}
          />
          {errors.prix_conso_ttc && <span className="error">{errors.prix_conso_ttc}</span>}
        </div>
        <div className="field-group">
          <label className="field-label">Prix détail TTC</label>
          <input
            type="number"
            step="0.01"
            min="0"
            inputMode="decimal"
            className={`input-base${errors.prix_detail_ttc ? " is-invalid" : ""}`}
            placeholder="0.00"
            value={value.prix_detail_ttc ?? ""}
            onChange={handleChange("prix_detail_ttc")}
          />
          {errors.prix_detail_ttc && <span className="error">{errors.prix_detail_ttc}</span>}
        </div>
      </div>
    </div>
  );
}
