import { NavLink } from 'react-router-dom'

const links = [
  { to: '/',          icon: '📊', label: 'Dashboard' },
  { to: '/expenses',  icon: '💳', label: 'Expenses'  },
  { to: '/analytics', icon: '📈', label: 'Analytics' },
]

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">💰</div>
        <div>
          <div className="sidebar-logo-text">SmartSpend</div>
          <div className="sidebar-logo-sub">Expense Tracker</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {links.map(({ to, icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
          >
            <span className="nav-icon">{icon}</span>
            {label}
          </NavLink>
        ))}
      </nav>

      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', padding: '0 12px' }}>
  
      </div>
    </aside>
  )
}
