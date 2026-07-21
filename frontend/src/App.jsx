import { useState } from 'react'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext.jsx'
import AuthLayout from './templates/AuthLayout.jsx'
import AuthForm from './organisms/AuthForm.jsx'
import VeilleMarcheModule from '../pages/VeilleMarcheModule.jsx'

function ProtectedApplication() {
  const { session, signIn, register, signOut } = useAuth()
  const [authMode, setAuthMode] = useState('signin')
  if (!session) {
    return (
      <AuthLayout>
        <AuthForm
          mode={authMode}
          onSubmit={authMode === 'signup' ? register : signIn}
          onSwitchMode={() => setAuthMode((mode) => mode === 'signin' ? 'signup' : 'signin')}
        />
      </AuthLayout>
    )
  }
  return <BrowserRouter><VeilleMarcheModule onSignOut={signOut} session={session} /></BrowserRouter>
}

export default function App() {
  return <AuthProvider><ProtectedApplication /></AuthProvider>
}
