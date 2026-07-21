/**
 * Validation centralisée du wizard de collecte.
 * Chaque fonction retourne un objet d'erreurs { champ: "message" }.
 * Un objet vide {} veut dire "pas d'erreur".
 */

export function validateVisiteForm(data) {
  const errors = {};

  if (!data.secteur) errors.secteur = "Le secteur est obligatoire.";
  if (!data.canal) errors.canal = "Le canal est obligatoire.";
  if (!data.ville) errors.ville = "La ville est obligatoire.";
  if (!data.adresse) errors.adresse = "L’adresse est obligatoire.";
  if (!data.nom?.trim()) errors.nom = "Le nom du magasin est obligatoire.";
  return errors;
}

/**
 * Valide une paire de prix pour un SKU.
 * Règles : si un des deux prix est renseigné, l'autre doit l'être aussi ;
 * les prix doivent être des nombres positifs ; le prix conso ne doit pas
 * dépasser le prix détail (incohérence probable de saisie).
 */
export function validateSkuPrice(value = {}, required = false) {
  const errors = {};
  const { prix_conso_ttc, prix_detail_ttc } = value;

  const consoFilled = prix_conso_ttc !== "" && prix_conso_ttc !== undefined && prix_conso_ttc !== null;
  const detailFilled = prix_detail_ttc !== "" && prix_detail_ttc !== undefined && prix_detail_ttc !== null;

  if (!consoFilled && !detailFilled) {
    if (required) {
      errors.prix_conso_ttc = "Prix conso obligatoire.";
      errors.prix_detail_ttc = "Prix détail obligatoire.";
    }
    return errors;
  }

  if (!consoFilled) errors.prix_conso_ttc = "Prix conso manquant.";
  else if (Number(prix_conso_ttc) <= 0) errors.prix_conso_ttc = "Doit être positif.";

  if (!detailFilled) errors.prix_detail_ttc = "Prix détail manquant.";
  else if (Number(prix_detail_ttc) <= 0) errors.prix_detail_ttc = "Doit être positif.";

  if (
    consoFilled &&
    detailFilled &&
    Number(prix_conso_ttc) > 0 &&
    Number(prix_detail_ttc) > 0 &&
    Number(prix_conso_ttc) > Number(prix_detail_ttc)
  ) {
    errors.prix_conso_ttc = "Le prix conso dépasse le prix détail — vérifie la saisie.";
  }

  return errors;
}

/**
 * Valide l'ensemble des relevés saisis à l'étape 4, avant de passer au
 * récapitulatif. Retourne { hasErrors, hasAtLeastOneLine, errorsBySkuId }.
 */
export function validateReleves(releves, requiredSkuIds = []) {
  const errorsBySkuId = {};
  let hasAtLeastOneLine = false;

  const skuIds = new Set([...Object.keys(releves), ...requiredSkuIds.map(String)]);
  skuIds.forEach((skuId) => {
    const value = releves[skuId] || {};
    const errs = validateSkuPrice(value, requiredSkuIds.map(String).includes(String(skuId)));
    if (Object.keys(errs).length > 0) errorsBySkuId[skuId] = errs;

    const consoFilled = value.prix_conso_ttc !== "" && value.prix_conso_ttc != null;
    const detailFilled = value.prix_detail_ttc !== "" && value.prix_detail_ttc != null;
    if (consoFilled && detailFilled) hasAtLeastOneLine = true;
  });

  return {
    hasErrors: Object.keys(errorsBySkuId).length > 0,
    hasAtLeastOneLine,
    errorsBySkuId,
  };
}

export function isVisiteFormValid(data) {
  return Object.keys(validateVisiteForm(data)).length === 0;
}
