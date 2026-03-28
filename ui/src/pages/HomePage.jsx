import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { getCompanies, deleteCompany } from '../api'
import CreateModal from '../components/CreateModal'
import CompanyCard from '../components/CompanyCard'
import './HomePage.css'

export default function HomePage() {
  const [companies, setCompanies] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [expandedId, setExpandedId] = useState(null)
  const newCardRef = useRef(null)
  const navigate = useNavigate()

  const fetchCompanies = async () => {
    try {
      const res = await getCompanies()
      setCompanies(res.data)
    } catch (err) {
      if (err.response?.status !== 401) {
        setError('Failed to load companies. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCompanies()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this company?')) return
    try {
      await deleteCompany(id)
      setCompanies((prev) => prev.filter((c) => c.id !== id))
    } catch {
      alert('Failed to delete company')
    }
  }

  const handleCreated = (company) => {
    setCompanies((prev) => [company, ...prev])
    setShowModal(false)
    setExpandedId(company.id)
    setTimeout(() => {
      newCardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 50)
  }

  return (
    <div className="home-container">
      <header className="home-header">
        <div className="header-left">
          <img src="/revo-logo.svg" alt="Revo" className="header-logo" />
        </div>
        <div className="header-right">
          <button className="create-btn" onClick={() => setShowModal(true)}>
            + Create
          </button>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="home-main">
        {loading ? (
          <div className="loading">Loading companies...</div>
        ) : error ? (
          <div className="error-state">
            <p>{error}</p>
            <button className="retry-btn" onClick={() => { setError(''); setLoading(true); fetchCompanies() }}>Retry</button>
          </div>
        ) : companies.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">
              <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 21h18M3 7v1a3 3 0 006 0V7m0 1a3 3 0 006 0V7m0 1a3 3 0 006 0V7H3l2-4h14l2 4M5 21V10.7M19 21V10.7" />
              </svg>
            </div>
            <h2>No companies yet</h2>
            <p>Click "Create" to add your first company and get AI-powered insights.</p>
          </div>
        ) : (
          <div className="companies-grid">
            {companies.map((company) => (
              <CompanyCard
                key={company.id}
                ref={company.id === expandedId ? newCardRef : null}
                company={company}
                onDelete={handleDelete}
                defaultExpanded={company.id === expandedId}
              />
            ))}
          </div>
        )}
      </main>

      {showModal && (
        <CreateModal
          onClose={() => setShowModal(false)}
          onCreated={handleCreated}
        />
      )}
    </div>
  )
}
