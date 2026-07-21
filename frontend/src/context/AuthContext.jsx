import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import client, { clearSession, readSession, writeSession } from '../utils/apiClient.js'

const AuthContext = createContext(null)
export function AuthProvider({ children }) {
  const [session, setSession] = useState(readSession)
  useEffect(() => {
    const expire = () => setSession(null)
    window.addEventListener('veille-marche:session-expired', expire)
    return () => window.removeEventListener('veille-marche:session-expired', expire)
  }, [])
  const authenticate = async (path, payload) => { const { data } = await client.post(path, payload); writeSession(data); setSession(data); return data }
  const value = useMemo(() => ({
    session,
    signIn: (payload) => authenticate('/auth/login/', { email: payload.email, password: payload.password }),
    register: (payload) => authenticate('/auth/register/', payload),
    forgotPassword: (email) => client.post('/auth/forgot-password/', { email }),
    me: () => client.get('/auth/me/'),
    signOut: async () => { try { if (session?.refresh) await client.post('/auth/logout/', { refresh: session.refresh }) } finally { clearSession(); setSession(null) } },
  }), [session])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
export const useAuth = () => useContext(AuthContext)
