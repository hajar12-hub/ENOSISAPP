/** Atome compatible avec l'API Select d'ENOSISAPP. */
export default function Select({ className = '', children, ...props }) {
  return <select className={`select-base ${className}`.trim()} {...props}>{children}</select>
}
