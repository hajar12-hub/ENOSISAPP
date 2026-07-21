import { useEffect, useState, useMemo } from "react";
import veilleMarcheApi from "../../utils/veilleMarcheApi";
import VeilleMarcheStepCard from "../../molecules/VeilleMarche/VeilleMarcheStepCard";
import VeilleMarcheSelectionItem from "../../molecules/VeilleMarche/VeilleMarcheSelectionItem";

export default function VeilleMarcheSousCategorieStep({ categorieId, onSelect }) {
  const [sousCategories, setSousCategories] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(null);

  const load = () => {
    if (!categorieId) return;
    setLoading(true);
    setLoadError(null);
    veilleMarcheApi
      .listSousCategories(categorieId)
      .then(setSousCategories)
      .catch((e) => setLoadError(e.normalized?.message || "Impossible de charger les sous-catégories."))
      .finally(() => setLoading(false));
  };

  useEffect(load, [categorieId]);

  const filtered = useMemo(
    () => sousCategories.filter((sc) => sc.nom.toLowerCase().includes(search.toLowerCase())),
    [sousCategories, search]
  );

  return (
    <div>
      <VeilleMarcheStepCard
        title="Choisir la sous-catégorie"
        description="La liste change selon la catégorie choisie."
      />

      <div className="field-group">
        <input
          className="input-base"
          placeholder="Rechercher une sous-catégorie"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {loading ? (
        <p className="cell-muted">Chargement…</p>
      ) : loadError ? (
        <div className="alert alert--error">
          {loadError}{" "}
          <button type="button" className="action-link" onClick={load}>Réessayer</button>
        </div>
      ) : (
        <div className="veille-marche-selection-list">
          {filtered.map((sc) => (
            <VeilleMarcheSelectionItem
              key={sc.id}
              title={sc.nom}
              onSelect={() => onSelect(sc)}
            />
          ))}
          {filtered.length === 0 && (
            <p className="cell-muted">Aucune sous-catégorie trouvée.</p>
          )}
        </div>
      )}
    </div>
  );
}
