import veilleMarcheApi from "./veilleMarcheApi";
import { getCompletedContext, getDraftContext } from "./veilleMarcheDraft";

const nameById = (items) => Object.fromEntries(items.map((item) => [item.id, item.nom]));

export async function loadVisiteRecord(visite) {
  const [magasin, secteurs, villes, canaux, adresses, releves] = await Promise.all([
    veilleMarcheApi.getMagasin(visite.magasin),
    veilleMarcheApi.listSecteurs(),
    veilleMarcheApi.listVilles(),
    veilleMarcheApi.listCanaux(),
    veilleMarcheApi.listAdresses(),
    veilleMarcheApi.listReleves(visite.id),
  ]);
  const context = visite.statut === "soumise" ? getCompletedContext(visite.id) : getDraftContext(visite.id);
  const labels = {
    secteur: nameById(secteurs)[magasin.secteur] || "—",
    ville: nameById(villes)[magasin.ville] || "—",
    canal: nameById(canaux)[magasin.canal] || "—",
    adresse: nameById(adresses)[magasin.adresse] || "—",
  };
  return { visite, magasin, releves, context, labels };
}

export const formatVisiteDate = (date) => new Date(date).toLocaleDateString("fr-MA");
