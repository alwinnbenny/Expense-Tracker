import { useEffect, useState } from 'react'
import { getExpenses, createExpense, updateExpense, deleteExpense, detectSuspicious } from '../api/expenses'
import SuspiciousBadge from '../components/SuspiciousBadge'
import ExpenseForm from '../components/ExpenseForm'

export default function Expenses() {
  const [expenses, setExpenses]   = useState([])
  const [loading, setLoading]     = useState(true)
  const [formOpen, setFormOpen]   = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [warning, setWarning]     = useState(null)
  const [scanning, setScanning]   = useState(false)

  const load = async () => {
    setLoading(true)
    try {
      const res = await getExpenses()
      setExpenses(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleSave = async (data) => {
    setWarning(null)
    if (editingItem) {
      const res = await updateExpense(editingItem.id, data)
      if (res.data.daily_limit_check?.exceeded) {
        setWarning(res.data.daily_limit_check)
      }
      setEditingItem(null)
    } else {
      const res = await createExpense(data)
      if (res.data.daily_limit_check?.exceeded) {
        setWarning(res.data.daily_limit_check)
      }
    }
    await load()
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this expense?')) {
      await deleteExpense(id)
      await load()
    }
  }

  const runScan = async () => {
    setScanning(true)
    try {
      const res = await detectSuspicious()
      alert(res.data.flagged_count > 0 
        ? `Scan complete: ${res.data.flagged_count} suspicious item(s) flagged.` 
        : 'Scan complete: No suspicious items found.')
      await load()
    } catch (err) {
      console.error(err)
    } finally {
      setScanning(false)
    }
  }

  return (
    <div className="fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Expenses</h1>
          <p className="page-subtitle">Manage and audit your logged transactions</p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button className="btn btn-secondary" onClick={runScan} disabled={scanning}>
            🔍 {scanning ? 'Scanning…' : 'Scan Suspicious'}
          </button>
          <button className="btn btn-primary" onClick={() => { setEditingItem(null); setFormOpen(true) }}>
            ➕ Log Expense
          </button>
        </div>
      </div>

      {warning && (
        <div className="limit-warning-banner danger" style={{ marginBottom: '24px' }}>
          ⚠️ <strong>Budget Alert!</strong> Daily limit exceeded on {warning.daily_total > warning.daily_limit ? 'this date' : ''}. 
          Spent: ₹{warning.daily_total.toFixed(2)} / Limit: ₹{warning.daily_limit.toFixed(2)} ({warning.percentage}%).
        </div>
      )}

      {loading ? (
        <div className="loading">
          <div className="spinner" />
          <span>Fetching transaction records…</span>
        </div>
      ) : (
        <div className="panel table-container">
          <table className="expense-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Category</th>
                <th>Description</th>
                <th>Amount</th>
                <th>Safety Check</th>
                <th style={{ textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {expenses.length > 0 ? (
                expenses.map((e) => (
                  <tr key={e.id}>
                    <td style={{ fontWeight: 600 }}>{e.date}</td>
                    <td><span className="badge btn-secondary" style={{ textTransform: 'none', border: '1px solid var(--border)' }}>{e.category}</span></td>
                    <td style={{ color: e.description ? 'var(--text-primary)' : 'var(--text-muted)', fontStyle: e.description ? 'normal' : 'italic' }}>
                      {e.description || 'No description'}
                    </td>
                    <td style={{ fontWeight: 700, color: 'var(--text-primary)' }}>₹{parseFloat(e.amount).toFixed(2)}</td>
                    <td>
                      <SuspiciousBadge reason={e.suspicious ? e.suspicious_reason : null} />
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <div style={{ display: 'inline-flex', gap: '8px' }}>
                        <button className="btn btn-secondary btn-sm" onClick={() => { setEditingItem(e); setFormOpen(true) }}>
                          Edit
                        </button>
                        <button className="btn btn-danger btn-sm" onClick={() => handleDelete(e.id)}>
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '40px 0', fontStyle: 'italic' }}>
                    No expenses logged. Click "Log Expense" to start.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {formOpen && (
        <ExpenseForm
          expense={editingItem}
          onClose={() => setFormOpen(false)}
          onSave={handleSave}
        />
      )}
    </div>
  )
}