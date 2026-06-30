import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getAnalytics, getSettings, updateSettings } from '../api/expenses'
import StatCard from '../components/StatCard'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from 'recharts'

export default function Dashboard() {
  const [analytics, setAnalytics] = useState(null)
  const [settings, setSettings]   = useState(null)
  const [limitInput, setLimitInput] = useState('')
  const [limitSaving, setLimitSaving] = useState(false)
  const [loading, setLoading] = useState(true)

  const load = async () => {
    try {
      const [aRes, sRes] = await Promise.all([getAnalytics(), getSettings()])
      setAnalytics(aRes.data)
      setSettings(sRes.data)
      setLimitInput(sRes.data.daily_limit ?? '')
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const saveLimit = async () => {
    setLimitSaving(true)
    try {
      await updateSettings({ daily_limit: limitInput === '' ? null : parseFloat(limitInput) })
      await load()
    } catch (err) {
      console.error(err)
    } finally {
      setLimitSaving(false)
    }
  }

  if (loading) return (
    <div className="loading fade-in">
      <div className="spinner" />
      <span>Loading dashboard…</span>
    </div>
  )

  const a = analytics
  const dailyLimit = settings?.daily_limit
  const todayStr = new Date().toISOString().slice(0, 10)
  const todayEntry = a?.daily_totals?.find(d => d.date === todayStr)
  const todayTotal = todayEntry?.total ?? 0
  const limitPct   = dailyLimit ? Math.min(100, (todayTotal / dailyLimit) * 100) : 0
  const limitColor = limitPct > 100 ? 'var(--accent-red)' : limitPct >= 80 ? 'var(--accent-amber)' : 'var(--accent-green)'
  const recentExpenses = a?.daily_totals ? [...(a.daily_totals)].reverse().slice(0, 5) : []

  return (
    <div className="fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Your financial overview at a glance</p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <Link to="/expenses" className="btn btn-primary">💳 Log Expense</Link>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          label="Total Spent"
          value={`₹${a?.overall_total?.toFixed(2) ?? '0.00'}`}
          sub="Accumulated expenses"
          accentColor="var(--primary)"
          icon="💰"
        />
        <StatCard
          label="Avg per Expense"
          value={`₹${a?.average_expense?.toFixed(2) ?? '0.00'}`}
          sub="Mean cost per item"
          accentColor="var(--accent-cyan)"
          icon="🧮"
        />
        <StatCard
          label="Total Count"
          value={a?.total_count ?? 0}
          sub="Logged expenses count"
          accentColor="var(--accent-green)"
          icon="🧾"
        />
        <StatCard
          label="Suspicious Flags"
          value={a?.suspicious_count ?? 0}
          sub="Flagged items"
          accentColor="var(--accent-red)"
          icon="🚨"
        />
      </div>

      <div className="dashboard-grid">
        <div className="panel" style={{ display: 'flex', flexDirection: 'column' }}>
          <h2 className="panel-title">Spending Trend</h2>
          <div style={{ width: '100%', height: 300, marginTop: 'auto' }}>
            {a?.spending_trend?.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={a.spending_trend} margin={{ top: 5, right: 20, left: -20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="month" stroke="var(--text-secondary)" tick={{ fontSize: 12 }} />
                  <YAxis stroke="var(--text-secondary)" tick={{ fontSize: 12 }} />
                  <Tooltip
                    contentStyle={{ background: '#111827', border: '1px solid var(--border)', borderRadius: 8 }}
                    labelStyle={{ color: 'var(--text-secondary)', fontSize: 12 }}
                    itemStyle={{ color: 'var(--text-primary)', fontWeight: 600 }}
                  />
                  <Line type="monotone" dataKey="total" stroke="var(--primary)" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
                No spending data logged yet.
              </div>
            )}
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
          <div className="panel limit-widget">
            <h2 className="panel-title">Daily Spending Limit</h2>
            <div className="limit-info">
              <span style={{ color: 'var(--text-secondary)' }}>Today's Total:</span>
              <span style={{ fontWeight: 700 }}>₹{todayTotal.toFixed(2)}</span>
            </div>
            {dailyLimit ? (
              <>
                <div className="progress-bar-bg">
                  <div className="progress-bar-fill" style={{ width: `${limitPct}%`, backgroundColor: limitColor }} />
                </div>
                <div className="limit-info" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  <span>{limitPct.toFixed(1)}% of limit</span>
                  <span>Limit: ₹{parseFloat(dailyLimit).toFixed(2)}</span>
                </div>
                {todayTotal > dailyLimit && (
                  <div className="limit-warning-banner danger">
                    ⚠️ You have exceeded your daily limit by ₹{(todayTotal - dailyLimit).toFixed(2)}!
                  </div>
                )}
                {todayTotal <= dailyLimit && todayTotal >= dailyLimit * 0.8 && (
                  <div className="limit-warning-banner warning">
                    ⚠️ Approaching daily limit! Remaining: ₹{(dailyLimit - todayTotal).toFixed(2)}
                  </div>
                )}
              </>
            ) : (
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontStyle: 'italic', marginBottom: '10px' }}>
                No daily spending limit configured.
              </div>
            )}

            <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
              <input
                type="number"
                placeholder="Set Limit (₹)"
                className="form-control"
                style={{ padding: '8px 12px', fontSize: '0.85rem' }}
                value={limitInput}
                onChange={(e) => setLimitInput(e.target.value)}
              />
              <button className="btn btn-secondary btn-sm" onClick={saveLimit} disabled={limitSaving}>
                {limitSaving ? 'Saving…' : 'Save'}
              </button>
            </div>
          </div>

          <div className="panel">
            <h2 className="panel-title">Recent Activity</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {recentExpenses.length > 0 ? (
                recentExpenses.map((day) => (
                  <div key={day.date} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>
                    <div>
                      <div style={{ fontSize: '0.9rem', fontWeight: 600 }}>{day.date}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                        {day.exceeded ? '🚨 Daily limit exceeded' : '✅ Within budget'}
                      </div>
                    </div>
                    <span style={{ fontSize: '1rem', fontWeight: 700, color: day.exceeded ? 'var(--accent-red)' : 'var(--text-primary)' }}>
                      ₹{day.total.toFixed(2)}
                    </span>
                  </div>
                ))
              ) : (
                <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic' }}>
                  No recent activities recorded.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}