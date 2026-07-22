import client from '../src/utils/apiClient.js'

const base = '/veille-marche'
const data = (request) => request.then((response) => response.data)

// Le référentiel change rarement pendant une session. Ce cache mémorise aussi
// la promesse en cours : deux montages React (notamment StrictMode en dev) ou
// deux écrans simultanés partagent donc la même requête HTTP.
const referentialCache = new Map()
const cached = (key, request) => {
  if (!referentialCache.has(key)) {
    const pending = request().catch((error) => {
      referentialCache.delete(key)
      throw error
    })
    referentialCache.set(key, pending)
  }
  return referentialCache.get(key)
}

export function clearReferentialCache() {
  referentialCache.clear()
}

export function apiMessage(error, fallback = 'Une erreur est survenue.') {
  const payload = error.response?.data
  if (typeof payload?.detail === 'string') return payload.detail
  if (payload && typeof payload === 'object') {
    const first = Object.values(payload).flat()[0]
    if (typeof first === 'string') return first
  }
  if (!error.response) return 'Impossible de contacter le serveur.'
  if (error.response.status === 403) return "Vous n'avez pas les droits nécessaires."
  if (error.response.status >= 500) return 'Erreur serveur. Réessayez dans un instant.'
  return fallback
}

const veilleMarcheApi = {
  secteurs: () => cached('secteurs', () => data(client.get(`${base}/secteurs/`))),
  villes: () => cached('villes', () => data(client.get(`${base}/villes/`))),
  categories: () => cached('categories', () => data(client.get(`${base}/categories/`))),
  sousCategories: (categorie) => cached(`sous-categories:${categorie}`, () => data(client.get(`${base}/sous-categories/`, { params: { categorie } }))),
  segments: (sousCategorie) => cached(`segments:${sousCategorie}`, () => data(client.get(`${base}/segments/`, { params: { sous_categorie: sousCategorie } }))),
  marques: (params) => cached(`marques:${JSON.stringify(params || {})}`, () => data(client.get(`${base}/marques/`, { params }))),
  skus: (marque) => cached(`skus:${marque}`, () => data(client.get(`${base}/skus/`, { params: { marque } }))),
  createMagasin: (payload) => data(client.post(`${base}/magasins/`, payload)),
  magasin: (id) => data(client.get(`${base}/magasins/${id}/`)),
  // La date de visite est volontairement détenue par le serveur (auto_now_add / timezone.now).
  createVisite: (magasin) => data(client.post(`${base}/visites/`, { magasin })),
  updateVisite: (id, payload) => data(client.patch(`${base}/visites/${id}/`, payload)),
  visite: (id) => data(client.get(`${base}/visites/${id}/`)),
  visites: (statut) => data(client.get(`${base}/visites/`, { params: statut ? { statut } : {} })),
  releves: (visite) => data(client.get(`${base}/releves/`, { params: { visite } })),
  saveReleves: (visite, releves, draft) => data(client.post(`${base}/releves/`, { releves }, { params: { visite, ...(draft ? { draft: 1 } : {}) } })),
}

export default veilleMarcheApi
