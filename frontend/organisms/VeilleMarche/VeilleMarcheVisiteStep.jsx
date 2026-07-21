import { useEffect, useState } from "react";
import veilleMarcheApi from "../../utils/veilleMarcheApi";
import { validateVisiteForm } from "../../utils/veilleMarcheValidation";

export default function VeilleMarcheVisiteStep({ data, onChange, touched, onTouch }) {
  const [secteurs, setSecteurs] = useState([]);
  const [canaux, setCanaux] = useState([]);
  const [villes, setVilles] = useState([]);
  const [adresses, setAdresses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(null);

  const loadReferentiel = () => {
    setLoading(true);
    setLoadError(null);
    Promise.all([
      veilleMarcheApi.listSecteurs(),
      veilleMarcheApi.listCanaux(),
      veilleMarcheApi.listVilles(),
      veilleMarcheApi.listAdresses(),
    ])
      .then(([s, c, v, a]) => {
        setSecteurs(s);
        setCanaux(c);
        setVilles(v);
        setAdresses(a);
        onChange((current) => ({
          ...current,
          canal: current.canal || "",
          canalLabel: current.canalLabel || "",
          adresse: current.adresse || "",
          adresseLabel: current.adresseLabel || "",
          nom: current.nom || "",
          date_visite: new Date().toISOString().slice(0, 10),
        }));
      })
      .catch((e) => setLoadError(e.normalized?.message || "Impossible de charger le référentiel."))
      .finally(() => setLoading(false));
  };

  // The reference lists are loaded once at step entry; the callback is a
  // parent state setter and deliberately remains stable for this workflow.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(loadReferentiel, []);

  const errors = validateVisiteForm(data);

  const update = (field, options = []) => (e) => {
    const selected = options.find((item) => item.id === e.target.value);
    onChange({ ...data, [field]: e.target.value, [`${field}Label`]: selected?.nom || "" });
  };

  const blur = (field) => () => onTouch && onTouch(field);

  const showError = (field) => touched && touched[field] && errors[field];

  const fieldClass = (field) => `select-base${showError(field) ? " is-invalid" : ""}`;

  return (
    <div>
      {loading ? (
        <p className="cell-muted">Chargement du référentiel…</p>
      ) : loadError ? (
        <div className="alert alert--error">
          {loadError}{" "}
          <button type="button" className="action-link" onClick={loadReferentiel}>
            Réessayer
          </button>
        </div>
      ) : (
        <div className="veille-marche-form">{!secteurs.length || !canaux.length || !villes.length || !adresses.length ? <div className="veille-marche-empty-state"><strong>Référentiel incomplet</strong><p>Aucune donnée n’est disponible pour démarrer une visite.</p><button type="button" className="button button--secondary" onClick={loadReferentiel}>Réessayer</button></div> : <>
          <div className="field-row">
            <div className="field-group" id="field-secteur">
              <label className="field-label">
                Secteur<span className="field-label__required">*</span>
              </label>
              <select
                className={fieldClass("secteur")}
                value={data.secteur || ""}
                onChange={update("secteur", secteurs)}
                onBlur={blur("secteur")}
              >
                <option value="">Choisir</option>
                {secteurs.map((s) => (
                  <option key={s.id} value={s.id}>{s.nom}</option>
                ))}
              </select>
              {showError("secteur") && <span className="error">{errors.secteur}</span>}
            </div>
            <div className="field-group" id="field-ville">
              <label className="field-label">
                Ville<span className="field-label__required">*</span>
              </label>
              <select
                className={fieldClass("ville")}
                value={data.ville || ""}
                onChange={update("ville", villes)}
                onBlur={blur("ville")}
              >
                <option value="">Choisir</option>
                {villes.map((v) => (
                  <option key={v.id} value={v.id}>{v.nom}</option>
                ))}
              </select>
              {showError("ville") && <span className="error">{errors.ville}</span>}
            </div>
            <div className="field-group"><label className="field-label">Canal<span className="field-label__required">*</span></label><select className={fieldClass("canal")} value={data.canal || ""} onChange={update("canal", canaux)} onBlur={blur("canal")}><option value="">Choisir</option>{canaux.map((item) => <option key={item.id} value={item.id}>{item.nom}</option>)}</select>{showError("canal") && <span className="error">{errors.canal}</span>}</div>
            <div className="field-group"><label className="field-label">Adresse<span className="field-label__required">*</span></label><select className={fieldClass("adresse")} value={data.adresse || ""} onChange={update("adresse", adresses)} onBlur={blur("adresse")}><option value="">Choisir</option>{adresses.map((item) => <option key={item.id} value={item.id}>{item.nom}</option>)}</select>{showError("adresse") && <span className="error">{errors.adresse}</span>}</div>
          </div>
          <div className="field-group"><label className="field-label">Nom du magasin<span className="field-label__required">*</span></label><input className={`input-base${showError("nom") ? " is-invalid" : ""}`} value={data.nom || ""} onChange={update("nom")} onBlur={blur("nom")} placeholder="Ex. Marjane Ain Sebaa" />{showError("nom") && <span className="error">{errors.nom}</span>}</div></>}
        </div>
      )}
    </div>
  );
}
