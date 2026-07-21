const cards = [
  ['new', '📋', 'Nouvelle visite', 'Démarrer une collecte terrain.'],
  ['drafts', '📝', 'Compléter un relevé', 'Reprendre un relevé sauvegardé.'],
  ['history', '📖', 'Historique', 'Consulter les relevés soumis.'],
  ['promotions', '🎯', 'Plan promotionnel', 'Explorer les opérations commerciales.'],
]
export default function HomePage({ onNavigate, onSignOut, message }) { return <main className="module-page"><header className="module-header"><img className="brand-logo brand-logo--header" src="/image_enosisapp.png" alt="Enosis"/><button className="text-button" onClick={onSignOut}>Déconnexion</button></header><section className="home-intro"><span>VEILLE MARCHÉ</span><h1>Votre centre de collecte</h1><p>Accédez rapidement à vos visites, brouillons, relevés et promotions.</p></section>{message && <p className="notice notice--success">{message}</p>}<section className="home-grid">{cards.map(([key, icon, title, description]) => <button className="home-card" key={key} onClick={() => onNavigate(key)}><i>{icon}</i><strong>{title}</strong><span>{description}</span><b>→</b></button>)}</section></main> }
