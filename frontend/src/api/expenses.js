import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getExpenses    = ()       => api.get('/expenses/')
export const createExpense  = (data)   => api.post('/expenses/', data)
export const updateExpense  = (id, d)  => api.put(`/expenses/${id}/`, d)
export const deleteExpense  = (id)     => api.delete(`/expenses/${id}/`)
export const getAnalytics   = ()       => api.get('/expenses/analytics/')
export const detectSuspicious = ()     => api.post('/expenses/detect_suspicious/')
export const getSettings    = ()       => api.get('/settings/')
export const updateSettings = (data)   => api.post('/settings/', data)
