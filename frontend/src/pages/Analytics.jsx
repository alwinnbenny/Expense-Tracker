import { useEffect, useState } from 'react'
import { getAnalytics, detectSuspicious } from '../api/expenses'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts'

const COLORS = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6']

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{ background: '#111827', border: '1px solid rgba(99,102,241,0.3)', borderRadius: 8, padding: '10px 14px' }}>
      <div style={{ color: '#94a3b8', fontSize: '0.8rem', marginBottom: 4 }}>{label}</div>
      <div style={{ color: '#f1f5f9', fontWeight: 700 }}>₹{payload[0].value?.toFixed(2)}</div>
    </div>
  )
}

export default function Analytics() {
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(true)
  const [scanning, setScanning] = useState(false)
  const [scanMsg, setScanMsg]   = useState(null)

  const load = async () => {
    setLoading(true)
    try {
      const res = await getAnalytics()
      setData(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const runScan = async () => {
    setScanning(true); setScanMsg(null)
    try {
      const res = await detectSuspicious()
      setScanMsg(res.data.flagged_count > 0 
        ? `${res.data.flagged_count} suspicious expense(s) detected.` 
        : 'No suspicious activity detected.')
      await load()
    } catch (err) {
      console.error(err)
    } finally {
      setScanning(false)
    }
  }

  if (loading) return (
    <div className="loading fade-in"><div className="spinner" /><span>Loading analytics…</span></div>
  )

  const catData = Object.entries(data.category_summary || {}).map(([name, total]) => ({ name, total }))
  const overallTotal = data.overall_total || 1

  return (
    <div className="fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Analytics</h1>
          <p className="page-subtitle">Deep dive insights and security auditing</p>
        </div>
        <button className="btn btn-secondary" onClick={runScan} disabled={scanning}>
          🔍 {scanning ? 'Scanning…' : 'Run Security Scan'}
        </button>
      </div>

      {scanMsg && (
        <div className={`limit-warning-banner ${data.suspicious_count > 0 ? 'danger' : 'warning'}`} style={{ marginBottom: '24px' }}>
          {scanMsg}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px', marginBottom: '30px' }}>
        <div className="panel">
          <h2 className="panel-title">Category Breakdown</h2>
          <div style={{ width: '100%', height: 260, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            {catData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={catData} dataKey="total" nameKey="name" cx="50%" cy="50%" outerRadius={80} innerRadius={40}>
                    {catData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                  <Legend verticalAlign="bottom" height={36} tick={{ fontSize: 11 }} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <span className="text-muted">No data available</span>
            )}
          </div>
        </div>

        <div className="panel">
          <h2 className="panel-title">Category Spending Share</h2>
          <div style={{ width: '100%', height: 260 }}>
            {catData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={catData} layout="vertical" margin={{ left: 10, right: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis type="number" stroke="var(--text-secondary)" />
                  <YAxis type="category" dataKey="name" stroke="var(--text-secondary)" width={80} tick={{ fontSize: 11 }} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="total" fill="var(--primary)" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <span className="text-muted">No data available</span>
            )}
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '30px', marginBottom: '30px' }}>
        <div className="panel">
          <h2 className="panel-title">Daily Expenditure & Limit Checks</h2>
          <div style={{ width: '100%', height: 260 }}>
            {data.daily_totals?.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.daily_totals} margin={{ left: -10, right: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="date" stroke="var(--text-secondary)" tick={{ fontSize: 10 }} />
                  <YAxis stroke="var(--text-secondary)" />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="total" fill="var(--primary-light)">
                    {data.daily_totals.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.exceeded ? 'var(--accent-red)' : 'var(--primary-light)'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <span className="text-muted">No daily records logged</span>
            )}
          </div>
        </div>

        <div className="panel" style={{ display: 'flex', flexDirection: 'column', justifycontent: 'space-between' }}>
          <h2 className="panel-title">Overview Stats</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', flex: 1, justifyContent: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Daily average:</span>
              <span style={{ fontWeight: 700 }}>₹{data.daily_average?.toFixed(2) ?? '0.00'}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Highest Category:</span>
              <span style={{ fontWeight: 700 }}>{data.highest_category ?? 'None'}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Lowest Category:</span>
              <span style={{ fontWeight: 700 }}>{data.lowest_category ?? 'None'}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="panel" style={{ marginBottom: '30px' }}>
        <h2 className="panel-title">🚨 Suspicious Activity Logs ({data.suspicious_count})</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {data.suspicious_expenses?.length > 0 ? (
            data.suspicious_expenses.map((e) => (
              <div key={e.id} style={{ display: 'flex', padding: '16px', borderRadius: 'var(--radius-md)', background: 'rgba(239, 68, 68, 0.05)', border: '1px solid rgba(239, 68, 68, 0.15)', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '4px' }}>
                    <span style={{ fontSize: '0.9rem', fontWeight: 700 }}>ID {e.id} ({e.category})</span>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{e.date}</span>
                  </div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontStyle: 'italic', marginBottom: '4px' }}>
                    {e.description || 'No description provided.'}
                  </div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--accent-red)', fontWeight: 600 }}>
                    Reason: {e.suspicious_reason}
                  </div>
                </div>
                <span style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--accent-red)' }}>
                  -₹{e.amount.toFixed(2)}
                </span>
              </div>
            ))
          ) : (
            <div style={{ padding: '20px 0', textalign: 'center', color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.9rem' }}>
              No suspicious spending patterns flagged in database.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}