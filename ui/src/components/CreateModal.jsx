import { useState } from 'react'
import { createCompany } from '../api'
import './CreateModal.css'

export default function CreateModal({ onClose, onCreated }) {
  const [name, setName] = useState('')
  const [hq, setHq] = useState('')
  const [website, setWebsite] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const res = await createCompany({ name, hq, website })
      onCreated(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create company. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Create Company</h2>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-form-group">
            <label htmlFor="company-name">Company Name</label>
            <input
              id="company-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Tesla"
              required
            />
          </div>
          <div className="modal-form-group">
            <label htmlFor="company-hq">HQ Information</label>
            <input
              id="company-hq"
              type="text"
              value={hq}
              onChange={(e) => setHq(e.target.value)}
              placeholder="e.g. Austin, Texas, USA"
              required
            />
          </div>
          <div className="modal-form-group">
            <label htmlFor="company-website">Company Website</label>
            <input
              id="company-website"
              type="text"
              value={website}
              onChange={(e) => setWebsite(e.target.value)}
              placeholder="e.g. https://tesla.com"
              required
            />
          </div>
          {error && <div className="modal-error">{error}</div>}
          <div className="modal-actions">
            <button type="button" className="cancel-btn" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? (
                <span className="spinner-wrap">
                  <span className="spinner"></span>
                  Generating with AI...
                </span>
              ) : (
                'Create'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
