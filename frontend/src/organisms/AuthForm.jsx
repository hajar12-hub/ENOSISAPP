import { useState } from 'react'
import Button from '../atoms/Button.jsx'

export default function AuthForm({ mode, onSubmit, onSwitchMode }) {
  const [values, setValues] = useState({ first_name: '', last_name: '', email: '', password: '', password_confirm: '' })
  const [error, setError] = useState(''); const [loading, setLoading] = useState(false)
  const signup = mode === 'signup'
  const update = (name) => (event) => setValues({ ...values, [name]: event.target.value })
  const submit = async (event) => { event.preventDefault(); setLoading(true); setError(''); try { await onSubmit(values) } catch (requestError) { const data = requestError.response?.data; setError(data?.detail || Object.values(data || {})[0]?.[0] || 'Une erreur est survenue.') } finally { setLoading(false) } }
  return <form className="auth-form" onSubmit={submit}>
    <h1>{signup ? <>Créer votre compte <span>eOne</span></> : <>Bienvenue sur <span>eOne</span></>}</h1>
    <p>{signup ? 'Créez vos accès Veille Marché.' : 'Connectez-vous pour accéder à Veille Marché.'}</p>
    {signup && <><input required placeholder="Prénom" value={values.first_name} onChange={update('first_name')}/><input required placeholder="Nom" value={values.last_name} onChange={update('last_name')}/></>}
    <input required type="email" placeholder="Email professionnel" value={values.email} onChange={update('email')}/>
    <input required type="password" placeholder="Mot de passe" value={values.password} onChange={update('password')}/>
    {signup && <input required type="password" placeholder="Confirmer le mot de passe" value={values.password_confirm} onChange={update('password_confirm')}/>} 
    {error && <p className="notice notice--error">{error}</p>}
    <Button variant="login" type="submit" disabled={loading}>{loading ? 'Connexion…' : signup ? 'Créer le compte' : 'Se connecter'}</Button>
    <button type="button" className="text-button" onClick={onSwitchMode}>{signup ? 'Déjà un compte ? Se connecter' : 'Créer un compte'}</button>
  </form>
}
