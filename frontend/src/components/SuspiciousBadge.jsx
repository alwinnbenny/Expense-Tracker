export default function SuspiciousBadge({ reason }) {
  if (!reason) return <span className="badge badge-ok">Clean</span>
  return (
    <span className="badge badge-suspicious" title={reason}>
      ⚠ Suspicious
    </span>
  )
}
