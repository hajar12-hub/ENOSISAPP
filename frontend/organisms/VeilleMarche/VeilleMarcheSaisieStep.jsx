import { useEffect, useState } from "react";
import veilleMarcheApi from "../../utils/veilleMarcheApi";
import VeilleMarcheStepCard from "../../molecules/VeilleMarche/VeilleMarcheStepCard";
import VeilleMarcheSkuPriceFields from "../../molecules/VeilleMarche/VeilleMarcheSkuPriceFields";

export default function VeilleMarcheSaisieStep({ sousCategorie, segment, releves, onChangeReleves }) {
  const [marques, setMarques] = useState([]);
  const [skusByMarque, setSkusByMarque] = useState({});
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(null);

  const load = () => {
    if (!sousCategorie) return;
    setLoading(true);
    setLoadError(null);
    veilleMarcheApi
      .resolveMarquesForSousCategorie(sousCategorie, segment?.id)
      .then(async (marquesResolved) => {
        setMarques(marquesResolved);
        const skusEntries = await Promise.all(
          marquesResolved.map(async (m) => [m.id, await veilleMarcheApi.listSkus(m.id)])
        );
        setSkusByMarque(Object.fromEntries(skusEntries));
      })
      .catch((e) => setLoadError(e.normalized?.message || "Impossible de charger les marques."))
      .finally(() => setLoading(false));
  };

  useEffect(load, [sousCategorie, segment]);

  const updateReleve = (skuId, patch) => {
    onChangeReleves({
      ...releves,
      [skuId]: { ...(releves[skuId] || {}), sku: skuId, ...patch },
    });
  };

  return (
    <div>
      <VeilleMarcheStepCard
        title="Saisie par blocs de marque"
        description="Chaque marque apparaît dans son bloc, et chaque SKU a ses 2 champs juste en dessous."
        badgeLabel="optimal"
        badgeTone="success"
      />

      {loading ? (
        <p className="cell-muted">Chargement des marques…</p>
      ) : loadError ? (
        <div className="alert alert--error">
          {loadError}{" "}
          <button type="button" className="action-link" onClick={load}>Réessayer</button>
        </div>
      ) : (
        marques.map((marque) => (
          <div key={marque.id} className="veille-marche-marque-block">
            <div className="veille-marche-marque-block__header">
              <div>
                <span className="cell-strong">{marque.nom}</span>
                {marque.groupLabel && <span className="cell-muted"> — {marque.groupLabel}</span>}
                <div className="cell-muted">
                  {(skusByMarque[marque.id] || []).length} SKU à relever
                </div>
              </div>
              <span className={`badge ${marque.concurrent ? "badge--warning" : "badge--success"}`}>
                {marque.concurrent ? "Concurrent" : "Interne"}
              </span>
            </div>

            {(skusByMarque[marque.id] || []).map((sku) => (
              <VeilleMarcheSkuPriceFields
                key={sku.id}
                skuLabel={sku.nom}
                marqueNom={marque.nom}
                value={releves[sku.id] || {}}
                onChange={(val) => updateReleve(sku.id, val)}
              />
            ))}
          </div>
        ))
      )}
    </div>
  );
}
