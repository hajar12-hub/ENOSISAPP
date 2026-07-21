import { useEffect, useState } from "react";
import veilleMarcheApi from "../../utils/veilleMarcheApi";
import VeilleMarcheStepCard from "../../molecules/VeilleMarche/VeilleMarcheStepCard";
import VeilleMarcheSelectionItem from "../../molecules/VeilleMarche/VeilleMarcheSelectionItem";

export default function VeilleMarcheCategorieStep({ data, onSelect }) {
  const [categories, setCategories] = useState([]);
  const [sousCategoriesCount, setSousCategoriesCount] = useState({});
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(null);

  const load = () => {
    setLoading(true);
    setLoadError(null);
    veilleMarcheApi
      .listCategories()
      .then(async (cats) => {
        setCategories(cats);
        const counts = {};
        await Promise.all(
          cats.map(async (c) => {
            const sc = await veilleMarcheApi.listSousCategories(c.id);
            counts[c.id] = sc.length;
          })
        );
        setSousCategoriesCount(counts);
      })
      .catch((e) => setLoadError(e.normalized?.message || "Impossible de charger les catégories."))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  return (
    <div>
      <VeilleMarcheStepCard
        title="Choisir la catégorie"
        description="Deux catégories seulement pour aller vite."
      />

      {loading ? (
        <p className="cell-muted">Chargement…</p>
      ) : loadError ? (
        <div className="alert alert--error">
          {loadError}{" "}
          <button type="button" className="action-link" onClick={load}>Réessayer</button>
        </div>
      ) : (
        <div className="veille-marche-selection-list">
          {categories.map((c) => (
            <VeilleMarcheSelectionItem
              key={c.id}
              title={c.nom}
              subtitle={`${sousCategoriesCount[c.id] ?? 0} sous-catégories`}
              onSelect={() => onSelect(c)}
              disabled={data.categorie === c.id}
            />
          ))}
        </div>
      )}
    </div>
  );
}
