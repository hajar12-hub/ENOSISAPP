// Même contrat que la configuration API d'ENOSISAPP : le frontend reste
// autonome tout en permettant une intégration ultérieure par variable d'env.
export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

export function buildApiUrl(path) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  if (API_BASE_URL === '/api') return `/api${normalizedPath}`
  return `${API_BASE_URL.replace(/\/$/, '')}${normalizedPath}`
}
