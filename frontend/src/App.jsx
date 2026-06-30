import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Sidebar    from './components/Sidebar'
import Dashboard  from './pages/Dashboard'
import Expenses   from './pages/Expenses'
import Analytics  from './pages/Analytics'

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/"          element={<Dashboard />} />
            <Route path="/expenses"  element={<Expenses />}  />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
