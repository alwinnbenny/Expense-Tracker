import { useState, useEffect } from 'react'

export default function ExpenseForm({ expense, onClose, onSave }) {
  const [amount, setAmount] = useState('')
  const [category, setCategory] = useState('')
  const [date, setDate] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (expense) {
      setAmount(expense.amount)
      setCategory(expense.category)
      setDate(expense.date)
      setDescription(expense.description ?? '')
    } else {
      setAmount('')
      setCategory('')
      setDate(new Date().toISOString().slice(0, 10))
      setDescription('')
    }
    setError(null)
  }, [expense])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    const parsedAmount = parseFloat(amount)
    if (isNaN(parsedAmount) || parsedAmount <= 0) {
      setError('Amount must be a positive number.')
      return
    }
    if (!category.trim()) {
      setError('Category is required.')
      return
    }
    if (!date) {
      setError('Date is required.')
      return
    }

    setSubmitting(true)
    try {
      await onSave({
        amount: parsedAmount,
        category: category.trim(),
        date,
        description: description.trim()
      })
      onClose()
    } catch (err) {
      setError(err.response?.data?.amount?.[0] || err.response?.data?.category?.[0] || 'Error saving expense. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content fade-in">
        <h2 className="panel-title" style={{ borderBottom: '1px solid var(--border)', paddingBottom: '12px', marginBottom: '20px' }}>
          {expense ? '✏️ Edit Expense' : '💵 Log New Expense'}
        </h2>
        
        {error && (
          <div className="limit-warning-banner danger" style={{ marginBottom: '16px' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Amount (₹) *</label>
            <input
              type="number"
              step="0.01"
              required
              className="form-control"
              placeholder="0.00"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Category *</label>
            <input
              type="text"
              required
              className="form-control"
              placeholder="e.g. Food, Transport, Rent"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Date *</label>
            <input
              type="date"
              required
              className="form-control"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Description (Optional)</label>
            <textarea
              className="form-control"
              placeholder="Add description..."
              rows="3"
              style={{ resize: 'none' }}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '30px' }}>
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Saving…' : 'Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}