export default function StatCard({ label, value, sub, accentColor = 'var(--primary)', icon }) {
  return (
    <div className="stat-card" style={{ '--accent-color': accentColor }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div className="stat-label">{label}</div>
          <div className="stat-value">{value}</div>
          {sub && <div className="stat-sub">{sub}</div>}
        </div>
        {icon && (
          <span style={{ fontSize: '1.6rem', opacity: 0.6 }}>{icon}</span>
        )}
      </div>
    </div>
  )
}
