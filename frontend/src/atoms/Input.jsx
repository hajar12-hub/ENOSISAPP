/** Atome compatible avec l'API Input d'ENOSISAPP. */
export default function Input({ className = '', ...props }) {
  return <input className={`input-base ${className}`.trim()} {...props} />
}
