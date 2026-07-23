import { useCallback, useEffect, useMemo, useState } from 'react'
import { NavLink, Navigate, Outlet, Route, Routes, useLocation, useNavigate, useParams } from 'react-router-dom'
import Button from '../src/atoms/Button.jsx'
import api, { apiMessage } from '../utils/veilleMarcheApi.js'

const NAV_ITEMS = [['/', 'Accueil', '⌂'], ['/nouveau-releve', 'Nouveau relevé', '＋'], ['/brouillons', 'Brouillons', '◫'], ['/historique', 'Historique', '◷'], ['/promotions', 'Promotions', '✦']]
const STEPS = ['visite', 'categorie', 'sous_categorie', 'format', 'sku', 'recap']
const STEP_LABELS = ['Secteur et ville', 'Catégorie', 'Sous-catégorie', 'Format', 'SKU', 'Récapitulatif']

function ModuleLayout({ onSignOut }) { return <div className="vm-shell"><aside className="vm-sidebar" aria-label="Navigation Veille Marché"><div className="vm-sidebar__brand"><img src="/image_enosisapp.png" alt="Enosis Group"/><div><strong>eOne</strong><span>Veille Marché</span></div></div><nav className="vm-sidebar__nav">{NAV_ITEMS.map(([to, label, icon]) => <NavLink key={to} to={`/veille-marche${to}`} end={to === '/'}><i aria-hidden="true">{icon}</i><span>{label}</span></NavLink>)}</nav><button type="button" className="vm-sidebar__logout" onClick={onSignOut}>Déconnexion</button></aside><main className="vm-main"><Outlet/></main></div> }
function PageHeader({ title, children }) { return <header className="page-header"><div><p className="eyebrow">VEILLE MARCHÉ</p><h1>{title}</h1></div>{children}</header> }
function Status({ value }) { const tone = ['Soumise', 'Active'].includes(value) ? 'success' : ['Brouillon', 'Planifiée'].includes(value) ? 'warning' : 'danger'; return <span className={`badge badge--${tone}`}>{value}</span> }
function Loader() { return <div className="loader" role="status"><span className="loader__dot"/>Chargement…</div> }
function EmptyState({ title, text }) { return <div className="empty-state"><div className="empty-state__icon">⌁</div><h2>{title}</h2><p>{text}</p></div> }
function formatDate(value) { return value ? new Date(value).toLocaleString('fr-MA', { dateStyle: 'medium', timeStyle: 'short' }) : '—' }
function label(items, id) { return items.find((item) => String(item.id) === String(id))?.nom || '—' }

function Home() { const navigate = useNavigate(); return <><section className="home-intro"><p className="eyebrow">VEILLE MARCHÉ</p><h1>Votre centre de collecte</h1><p>Pilotez vos relevés terrain, retrouvez vos brouillons et suivez vos opérations commerciales depuis un espace unique.</p></section><section className="home-grid">{[['/nouveau-releve', 'Nouveau relevé', 'Démarrer une collecte terrain.'], ['/brouillons', 'Brouillons', 'Reprendre un relevé sauvegardé.'], ['/historique', 'Historique', 'Consulter les relevés soumis.'], ['/promotions', 'Promotions', 'Explorer les opérations commerciales.']].map(([to, title, text]) => <button type="button" className="home-card" key={to} onClick={() => navigate(`/veille-marche${to}`)}><strong>{title}</strong><span>{text}</span><b>→</b></button>)}</section></> }

function VisitList({ statut, title, emptyTitle, emptyText }) { const [items, setItems] = useState([]); const [loading, setLoading] = useState(true); const [error, setError] = useState(''); const navigate = useNavigate(); const location = useLocation(); useEffect(() => { api.visites(statut).then(setItems).catch((e) => setError(apiMessage(e))).finally(() => setLoading(false)) }, [statut]); return <><PageHeader title={title}/>{location.state?.successMessage && <div className="alert alert--success">{location.state.successMessage}</div>}{loading ? <Loader/> : error ? <div className="alert alert--error">{error}</div> : !items.length ? <EmptyState title={emptyTitle} text={emptyText}/> : <div className="table-card"><div className="table-scroll"><table className="data-table"><thead><tr><th>Date automatique</th><th>Point de vente</th><th>Statut</th><th/></tr></thead><tbody>{items.map((visit) => <tr key={visit.id}><td>{formatDate(visit.date_visite || visit.created_at)}</td><td><button type="button" className="text-button" onClick={() => navigate(statut === 'brouillon' ? `/veille-marche/nouveau-releve/${visit.id}` : `/veille-marche/historique/${visit.id}`)}>{visit.magasin_nom || 'Point de vente'}</button></td><td><Status value={visit.statut === 'soumise' ? 'Soumise' : 'Brouillon'}/></td><td><Button size="sm" variant="secondary" onClick={() => navigate(statut === 'brouillon' ? `/veille-marche/nouveau-releve/${visit.id}` : `/veille-marche/historique/${visit.id}`)}>{statut === 'brouillon' ? 'Compléter' : 'Voir le relevé'}</Button></td></tr>)}</tbody></table></div></div>}</> }

function WizardProgress({ current }) { const index = STEPS.indexOf(current); return <ol className="wizard-progress">{STEPS.map((name, i) => <li key={name} className={i <= index ? (i === index ? 'is-current' : 'is-complete') : ''}><span>{i + 1}</span><small>{STEP_LABELS[i]}</small></li>)}</ol> }
function SelectionCards({ items = [], onSelect, icon = '◈', empty = 'Aucune donnée disponible.' }) { return <div className="selection-cards">{items.length ? items.map((item) => <button type="button" className="selection-card" key={item.id} onClick={() => onSelect(item)}><i>{icon}</i><strong>{item.nom}</strong><span>Choisir et continuer</span><b>→</b></button>) : <EmptyState title="Aucun élément" text={empty}/>}</div> }
function FieldStep({ title, text, fieldLabel = '', value, items = [], onChange }) {
  return <div className="visit-step"><div className="step-heading"><span className="step-heading__icon">⌖</span><div><h2>{title}</h2><p>{text}</p></div></div><label className="select-card"><span>{fieldLabel}</span><select value={value} onChange={(event) => onChange(event.target.value)}><option value="">Choisir {fieldLabel.toLowerCase()}</option>{items.map((item) => <option key={item.id} value={item.id}>{item.nom}</option>)}</select></label></div>
}
function VisitSetup({ form, secteurs, villes, onChange }) { return <div className="visit-step"><div className="step-heading"><span className="step-heading__icon">⌖</span><div><h2>Où effectuez-vous le relevé ?</h2><p>Choisissez le secteur et la ville. </p></div></div><div className="selection-grid"><label className="select-card"><span>Secteur</span><select value={form.secteur} onChange={(event) => onChange('secteur', event.target.value)}><option value="">Choisir secteur</option>{secteurs.map((item) => <option key={item.id} value={item.id}>{item.nom}</option>)}</select></label><label className="select-card"><span>Ville</span><select value={form.ville} onChange={(event) => onChange('ville', event.target.value)}><option value="">Choisir ville</option>{villes.map((item) => <option key={item.id} value={item.id}>{item.nom}</option>)}</select></label></div></div> }

function SkuFields({ brands, entries, setEntries, category, subcategory }) {
  if (!brands.length) return <EmptyState title="Aucun SKU" text="Cette sous-catégorie ne contient aucun produit dans le référentiel."/>
  const update = (sku, brand, key, value) => setEntries((current) => ({ ...current, [sku.id]: { ...(current[sku.id] || { sku: sku.id, sku_nom: sku.nom, marque_nom: brand.nom, categorie_nom: category.nom, sous_categorie: subcategory.id, sous_categorie_nom: subcategory.nom, segment_nom: brand.segment_nom || '' }), [key]: value } }))
  const toggle = (sku, brand, checked) => { if (checked) update(sku, brand, 'prix_conso_ttc', ''); else setEntries((current) => Object.fromEntries(Object.entries(current).filter(([id]) => id !== String(sku.id)))) }
  return <div>{brands.map((brand) => <section className="sku-block" key={brand.id}><header><div><h2>{brand.nom}</h2><p>{brand.segment_nom ? `Segment : ${brand.segment_nom}` : 'Marque'}</p></div>{brand.concurrent && <Status value="Concurrent"/>}</header>{brand.skus.map((sku) => { const value = entries[sku.id]; return <article className="sku-row sku-row--expanded" key={sku.id}><label className="sku-select"><input type="checkbox" checked={Boolean(value)} onChange={(event) => toggle(sku, brand, event.target.checked)}/><strong>{sku.nom}</strong></label>{value && <><input required type="number" min="0.01" step="0.01" placeholder="Prix conso TTC *" value={value.prix_conso_ttc ?? ''} onChange={(e) => update(sku, brand, 'prix_conso_ttc', e.target.value)}/><input required type="number" min="0.01" step="0.01" placeholder="Prix détail TTC *" value={value.prix_detail_ttc ?? ''} onChange={(e) => update(sku, brand, 'prix_detail_ttc', e.target.value)}/></>}</article> })}</section>)}</div>
}

function Recap({ record, store, selections, entries, categories, subcategories, user, readOnly = false }) {
  const rows = Object.values(entries); const userName = [user?.first_name, user?.last_name].filter(Boolean).join(' ') || user?.email || 'Utilisateur connecté'; const grouped = categories.map((category) => ({ category, subs: subcategories.filter((sub) => String(sub.categorie) === String(category.id)) })).filter(({ subs }) => subs.length)
  return <div className="recap-dashboard"><header className="recap-hero"><div><p className="eyebrow">{readOnly ? 'RELEVÉ SOUMIS' : 'VALIDATION FINALE'}</p><h2>{readOnly ? 'Consultation en lecture seule.' : 'Votre relevé est prêt à être vérifié.'}</h2><p>Toutes les informations collectées sont regroupées ci-dessous.</p></div><Status value={record?.statut === 'soumise' ? 'Soumise' : 'Brouillon'}/></header><section className="recap-section"><h3>Informations générales</h3><div className="recap-grid"><Summary label="Date automatique du relevé" value={formatDate(record?.date_visite || record?.created_at)}/><Summary label="Utilisateur connecté" value={userName}/><Summary label="Statut" value={record?.statut === 'soumise' ? 'Soumise' : 'Brouillon'}/><Summary label="Secteur" value={store?.secteur_nom || selections.secteur_nom}/><Summary label="Ville" value={store?.ville_nom || selections.ville_nom}/><Summary label="Magasin" value={store?.nom || record?.magasin_nom || selections.magasin_nom}/></div></section><section className="recap-section"><h3>Couverture du relevé</h3><div className="coverage-grid">{grouped.map(({ category, subs }) => <article key={category.id}><strong>{category.nom}</strong>{subs.map((sub) => <span key={sub.id} className={rows.some((row) => String(row.sous_categorie) === String(sub.id) || row.sous_categorie_nom === sub.nom) ? 'is-done' : ''}>{sub.nom}</span>)}</article>)}</div></section><section className="recap-section"><h3>SKU et prix relevés</h3><div className="table-card recap-table"><div className="table-scroll"><table className="data-table"><thead><tr><th>Catégorie</th><th>Sous-catégorie</th><th>Segment</th><th>Marque</th><th>SKU</th><th>Prix conso</th><th>Prix détail</th></tr></thead><tbody>{rows.length ? rows.map((row) => <tr key={row.sku}><td>{row.categorie_nom || '—'}</td><td>{row.sous_categorie_nom || '—'}</td><td>{row.segment_nom || '—'}</td><td>{row.marque_nom || '—'}</td><td>{row.sku_nom || row.sku}</td><td>{row.prix_conso_ttc}</td><td>{row.prix_detail_ttc}</td></tr>) : <tr><td colSpan="7">Aucun SKU renseigné.</td></tr>}</tbody></table></div></div></section></div>
}
function Summary({ label, value }) { return <p><span>{label}</span>{value || '—'}</p> }

function Wizard({ user }) {
  const { visitId } = useParams()
  const navigate = useNavigate()
  const [step, setStep] = useState('visite')
  const [options, setOptions] = useState({ secteurs: [], villes: [], categories: [], subcategories: [] })
  const [form, setForm] = useState({ secteur: '', ville: '' })
  const [record, setRecord] = useState(null)
  const [store, setStore] = useState(null)
  const [currentCategory, setCurrentCategory] = useState(null)
  const [currentSubcategory, setCurrentSubcategory] = useState(null)
  const [formats, setFormats] = useState([])
  const [currentFormat, setCurrentFormat] = useState(null)
  const [brands, setBrands] = useState([])
  const [entries, setEntries] = useState({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const hydrateBrands = useCallback(async (subcategory, format = null) => {
    const result = await api.marques(format ? { segment: format.id } : { sous_categorie: subcategory.id })
    const hydrated = await Promise.all(result.map(async (brand) => ({
      ...brand,
      segment_nom: format?.nom || '',
      skus: await api.skus(brand.id),
    })))
    setBrands(hydrated)
  }, [])

  const openSubcategory = useCallback(async (subcategory, categories, updateProgress = true) => {
    const category = categories.find((item) => String(item.id) === String(subcategory.categorie))
    setCurrentCategory(category || null)
    setCurrentSubcategory(subcategory)
    setCurrentFormat(null)
    if (category?.nom === 'Papier') {
      const availableFormats = await api.segments(subcategory.id)
      setFormats(availableFormats)
      if (updateProgress && record) await api.updateVisite(record.id, { etape: 'format' })
      go('format')
      return
    }
    await hydrateBrands(subcategory)
    if (updateProgress && record) await api.updateVisite(record.id, { etape: 'sku' })
    go('sku')
  }, [hydrateBrands, record])

  useEffect(() => {
    let alive = true
    Promise.all([api.secteurs(), api.villes(), api.categories(), api.sousCategories()]).then(async ([secteurs, villes, categories, subcategories]) => {
      if (!alive) return
      setOptions({ secteurs, villes, categories, subcategories })
      if (!visitId) return
      const visit = await api.visite(visitId)
      const [releves, magasin] = await Promise.all([api.releves(visitId), api.magasin(visit.magasin)])
      if (!alive) return
      setRecord(visit)
      setStore(magasin)
      setForm({ secteur: magasin.secteur, ville: magasin.ville })
      setEntries(Object.fromEntries(releves.map((row) => [row.sku, row])))
      const completedSubcategories = new Set(releves.filter((row) => Number(row.prix_conso_ttc) > 0 && Number(row.prix_detail_ttc) > 0).map((row) => String(row.sous_categorie)))
      const firstIncomplete = subcategories.find((subcategory) => !completedSubcategories.has(String(subcategory.id)))
      if (firstIncomplete) await openSubcategory(firstIncomplete, categories, false)
      else go('recap')
    }).catch((e) => alive && setError(apiMessage(e))).finally(() => alive && setLoading(false))
    return () => { alive = false }
  }, [visitId])

  const go = (next) => { setError(''); setStep(next) }
  const validRows = useMemo(() => Object.values(entries).filter((row) => Number(row.prix_conso_ttc) > 0 && Number(row.prix_detail_ttc) > 0), [entries])
  const incomplete = useMemo(() => options.subcategories.find((sub) => !validRows.some((row) => String(row.sous_categorie) === String(sub.id))), [options.subcategories, validRows])
  const payload = () => validRows.map(({ sku, prix_conso_ttc, prix_detail_ttc }) => ({ sku, prix_conso_ttc, prix_detail_ttc }))

  const createRecord = async () => {
    if (record) return go('categorie')
    if (!form.secteur || !form.ville) return setError('Veuillez sélectionner un secteur et une ville.')
    setSaving(true)
    try {
      const magasin = await api.createMagasin({ secteur: form.secteur, ville: form.ville })
      const visit = await api.createVisite(magasin.id)
      await api.updateVisite(visit.id, { etape: 'categorie' })
      setStore(magasin)
      setRecord({ ...visit, etape: 'categorie' })
      go('categorie')
    } catch (e) { setError(apiMessage(e)) } finally { setSaving(false) }
  }

  const selectCategory = (category) => { setCurrentCategory(category); go('sous_categorie') }
  const selectSubcategory = async (subcategory) => {
    setSaving(true)
    try {
      await openSubcategory(subcategory, options.categories)
    } catch (e) { setError(apiMessage(e)) } finally { setSaving(false) }
  }
  const selectFormat = async (format) => {
    setCurrentFormat(format)
    setSaving(true)
    try {
      await hydrateBrands(currentSubcategory, format)
      await api.updateVisite(record.id, { etape: 'sku' })
      go('sku')
    } catch (e) { setError(apiMessage(e)) } finally { setSaving(false) }
  }

  const persist = async (submit = false) => {
    if (!record) return
    if (Object.values(entries).some((row) => !Number(row.prix_conso_ttc) || !Number(row.prix_detail_ttc))) return setError('Veuillez compléter les deux prix pour chaque SKU sélectionné.')
    if (submit && incomplete) return setError(`Veuillez compléter la sous-catégorie « ${incomplete.nom} ».`)
    setSaving(true)
    try {
      await api.saveReleves(record.id, payload(), !submit)
      if (submit) navigate('/veille-marche/historique', { state: { successMessage: 'Relevé soumis avec succès.' } })
      else {
        await api.updateVisite(record.id, { etape: 'recap' })
        navigate('/veille-marche/brouillons', { state: { successMessage: 'Brouillon sauvegardé avec succès.' } })
      }
    } catch (e) { setError(apiMessage(e)) } finally { setSaving(false) }
  }

  const nextPending = async () => {
    if (!record) return
    const next = incomplete
    if (!next) return go('recap')
    setSaving(true)
    try {
      await api.saveReleves(record.id, payload(), true)
      await openSubcategory(next, options.categories)
    } catch (e) { setError(apiMessage(e)) } finally { setSaving(false) }
  }

  const back = () => {
    if (step === 'sku') return go(currentFormat ? 'format' : 'sous_categorie')
    if (step === 'format') return go('sous_categorie')
    if (step === 'sous_categorie') return go('categorie')
    if (step === 'categorie') return go('visite')
    if (step === 'recap') return currentSubcategory && brands.length ? go('sku') : go('categorie')
  }

  if (loading) return <Loader/>
  const categorySubs = currentCategory ? options.subcategories.filter((item) => String(item.categorie) === String(currentCategory.id)) : []
  return <><PageHeader title="Nouveau relevé"/>{error && <div className="alert alert--error">{error}</div>}<section className="wizard-card"><WizardProgress current={step}/><div className="wizard-body">{step === 'visite' && <VisitSetup form={form} secteurs={options.secteurs} villes={options.villes} onChange={(key, value) => setForm((current) => ({ ...current, [key]: value }))}/>} {step === 'categorie' && <SelectionCards items={options.categories} onSelect={selectCategory}/>} {step === 'sous_categorie' && <SelectionCards items={categorySubs} onSelect={selectSubcategory} icon="◇" empty="Aucune sous-catégorie pour cette catégorie."/>} {step === 'format' && <SelectionCards items={formats} onSelect={selectFormat} icon="◫" empty="Aucun format SKU pour cette sous-catégorie."/>} {step === 'sku' && <SkuFields brands={brands} entries={entries} setEntries={setEntries} category={currentCategory} subcategory={currentSubcategory}/>} {step === 'recap' && <Recap record={record} store={store} selections={{ secteur_nom: label(options.secteurs, form.secteur), ville_nom: label(options.villes, form.ville) }} entries={entries} categories={options.categories} subcategories={options.subcategories} user={user}/>}</div>{step === 'recap' ? <div className="wizard-actions wizard-actions--recap"><Button variant="secondary" onClick={back} disabled={saving}>Retour</Button><Button variant="secondary" onClick={() => persist(false)} disabled={saving}>Sauvegarder le brouillon</Button><Button onClick={() => persist(true)} disabled={saving}>Soumettre</Button><Button variant="secondary" onClick={nextPending} disabled={saving}>{incomplete ? 'Passer à la catégorie suivante' : 'Toutes les catégories sont complétées'}</Button></div> : <div className="wizard-actions"><Button variant="secondary" onClick={back} disabled={saving} style={{ visibility: step === 'visite' ? 'hidden' : 'visible' }}>Retour</Button>{step === 'visite' && <Button onClick={createRecord} disabled={saving}>{saving ? 'Enregistrement…' : 'Continuer'}</Button>}{step === 'sku' && <Button onClick={() => go('recap')} disabled={saving}>Continuer</Button>}</div>}</section></> }

function Detail({ user }) { const { visitId } = useParams(); const navigate = useNavigate(); const [state, setState] = useState({ loading: true, record: null, store: null, rows: [], categories: [], subs: [] }); useEffect(() => { let alive = true; Promise.all([api.visite(visitId), api.releves(visitId), api.categories()]).then(async ([record, rows, categories]) => { const store = await api.magasin(record.magasin); if (!alive) return; const subs = [...new Map(rows.filter((row) => row.sous_categorie_nom).map((row) => [row.sous_categorie || row.sous_categorie_nom, { id: row.sous_categorie || row.sous_categorie_nom, nom: row.sous_categorie_nom, categorie: categories.find((category) => category.nom === row.categorie_nom)?.id }])).values()]; setState({ loading: false, record, store, rows: Object.fromEntries(rows.map((row) => [row.sku, row])), categories, subs }) }).catch(() => alive && setState((old) => ({ ...old, loading: false }))); return () => { alive = false } }, [visitId]); if (state.loading) return <Loader/>; return <><PageHeader title="Détail du relevé"><Button variant="secondary" onClick={() => navigate('/veille-marche/historique')}>Retour</Button></PageHeader>{state.record ? <Recap record={state.record} store={state.store} selections={{}} entries={state.rows} categories={state.categories} subcategories={state.subs} user={user} readOnly/> : <EmptyState title="Relevé introuvable" text="Ce relevé n’est plus accessible."/>}</> }
function Promotions() { const promotions = [{ name: 'Offre rentrée MIO', status: 'Active', period: '01/09 — 30/09', discount: '15%', category: 'Détergent', brand: 'MIO', sku: '500gr, 1Kg' }, { name: 'Prix spécial Papillon', status: 'Planifiée', period: '15/08 — 15/09', discount: '10%', category: 'Papier', brand: 'Papillon', sku: '4, 12' }]; return <><PageHeader title="Promotions"/><div className="promotion-grid">{promotions.map((item) => <article key={item.name} className="promotion-card"><Status value={item.status}/><h2>{item.name}</h2><p>{item.period} · {item.discount}</p><dl><dt>Catégorie</dt><dd>{item.category}</dd><dt>Marque</dt><dd>{item.brand}</dd><dt>SKU</dt><dd>{item.sku}</dd></dl></article>)}</div></> }
export default function VeilleMarcheModule({ onSignOut, session }) { return <Routes><Route path="/veille-marche" element={<ModuleLayout onSignOut={onSignOut}/> }><Route index element={<Home/>}/><Route path="nouveau-releve" element={<Wizard user={session?.user}/>}/><Route path="nouveau-releve/:visitId" element={<Wizard user={session?.user}/>}/><Route path="brouillons" element={<VisitList statut="brouillon" title="Brouillons" emptyTitle="Aucun brouillon" emptyText="Vos relevés sauvegardés apparaîtront ici."/>}/><Route path="historique" element={<VisitList statut="soumise" title="Historique" emptyTitle="Aucun relevé soumis" emptyText="Les relevés soumis apparaîtront ici en lecture seule."/>}/><Route path="historique/:visitId" element={<Detail user={session?.user}/>}/><Route path="promotions" element={<Promotions/>}/></Route><Route path="*" element={<Navigate to="/veille-marche" replace/>}/></Routes> }