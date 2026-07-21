import VeilleMarcheStepCard from "../../molecules/VeilleMarche/VeilleMarcheStepCard";
import VeilleMarcheSummaryField from "../../molecules/VeilleMarche/VeilleMarcheSummaryField";

export default function VeilleMarcheRecapStep({ labels, releves, error }) {
  const lignesRemplies = Object.values(releves).filter(
    (r) => r.prix_conso_ttc && r.prix_detail_ttc
  ).length;
  const totalLignes = Object.keys(releves).length;

  return (
    <div>
      <VeilleMarcheStepCard
        title="Récapitulatif"
        description="Vérifie les informations avant de soumettre le relevé."
        badgeLabel="prêt"
        badgeTone="success"
      />

      <div className="veille-marche-recap-grid">
        <VeilleMarcheSummaryField label="Secteur" value={labels.secteur} />
        <VeilleMarcheSummaryField label="Magasin" value={labels.magasin} />
        <VeilleMarcheSummaryField label="Canal" value={labels.canal} />
        <VeilleMarcheSummaryField label="Catégorie" value={labels.categorie} />
        <VeilleMarcheSummaryField label="Sous-catégorie" value={labels.sousCategorie} />
        <VeilleMarcheSummaryField label="Segment" value={labels.segment} />
        <VeilleMarcheSummaryField label="Lignes SKU" value={totalLignes} />
        <VeilleMarcheSummaryField label="Lignes remplies" value={lignesRemplies} />
      </div>

      {lignesRemplies === 0 && (
        <div className="alert alert--warning">
          Aucune ligne n'est encore remplie — renseigne au moins un prix avant de soumettre.
        </div>
      )}

      {error && <div className="alert alert--error">{error}</div>}
    </div>
  );
}
