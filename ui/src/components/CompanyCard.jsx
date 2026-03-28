import { useState, forwardRef } from 'react'
import './CompanyCard.css'

const CompanyCard = forwardRef(function CompanyCard({ company, onDelete, defaultExpanded = false }, ref) {
  const [expanded, setExpanded] = useState(defaultExpanded)

  const formatSummary = (text) => {
    if (!text) return null
    return text.split('\n').filter(Boolean).map((line, i) => (
      <li key={i}>{line.replace(/^[•\-]\s*/, '')}</li>
    ))
  }

  return (
    <div className="company-card" ref={ref}>
      <div className="card-header" onClick={() => setExpanded(!expanded)}>
        <div className="card-info">
          <h3>{company.name}</h3>
          <div className="card-meta">
            <span className="meta-item">{company.hq}</span>
            <span className="meta-divider">|</span>
            <a
              href={company.website.startsWith('http') ? company.website : `https://${company.website}`}
              target="_blank"
              rel="noopener noreferrer"
              className="meta-link"
              onClick={(e) => e.stopPropagation()}
            >
              {company.website}
            </a>
          </div>
        </div>
        <div className="card-actions">
          <button
            className="delete-btn"
            onClick={(e) => { e.stopPropagation(); onDelete(company.id) }}
            title="Delete"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
          </button>
          <svg className={`expand-icon ${expanded ? 'expanded' : ''}`} width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
      </div>

      {expanded && (
        <div className="card-details">
          <div className="summary-section">
            <h4>Company Summary</h4>
            <ul>{formatSummary(company.summary)}</ul>
          </div>

          {company.competitors?.length > 0 && (
            <div className="competitors-section">
              <h4>Competitors ({company.competitors.length})</h4>
              <div className="competitors-grid">
                {company.competitors.map((comp) => (
                  <div key={comp.id} className="competitor-item">
                    <h5>{comp.name}</h5>
                    <ul>{formatSummary(comp.summary)}</ul>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="card-footer">
            <span className="created-at">
              Created: {new Date(company.created_at).toLocaleDateString('en-US', {
                year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
              })}
            </span>
          </div>
        </div>
      )}
    </div>
  )
})

export default CompanyCard
