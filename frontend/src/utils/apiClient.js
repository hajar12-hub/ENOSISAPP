import axios from 'axios'
import { API_BASE_URL } from '../config/api.js'

const SESSION_KEY = 'veille-marche.session'
export const readSession = () => {
  try { return JSON.parse(localStorage.getItem(SESSION_KEY) || 'null') } catch { return null }
}
export const writeSession = (session) => localStorage.setItem(SESSION_KEY, JSON.stringify(session))
export const clearSession = () => localStorage.removeItem(SESSION_KEY)

const client = axios.create({ baseURL: API_BASE_URL, timeout: 15000 })
const refreshClient = axios.create({ baseURL: API_BASE_URL, timeout: 15000 })

function notifySessionExpired() {
  window.dispatchEvent(new Event('veille-marche:session-expired'))
}

client.interceptors.request.use((config) => { const token = readSession()?.access; if (token) config.headers.Authorization = `Bearer ${token}`; return config })
let refreshing = null
client.interceptors.response.use((response) => response, async (error) => {
  const request = error.config
  if (![401, 403].includes(error.response?.status) || request?._retry || request?.skipAuthRefresh) return Promise.reject(error)
  const session = readSession()
  if (!session?.refresh) { clearSession(); notifySessionExpired(); return Promise.reject(error) }
  request._retry = true
  try {
    refreshing ||= refreshClient.post('/auth/refresh/', { refresh: session.refresh }, { skipAuthRefresh: true }).then(({ data }) => { const next = { ...session, ...data }; writeSession(next); return next.access }).finally(() => { refreshing = null })
    request.headers.Authorization = `Bearer ${await refreshing}`
    return client(request)
  } catch (refreshError) { clearSession(); notifySessionExpired(); return Promise.reject(refreshError) }
})
export default client
