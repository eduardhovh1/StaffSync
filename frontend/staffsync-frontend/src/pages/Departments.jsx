import { useEffect, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

function Departments() {
  const [departments, setDepartments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_URL}/api/departments/`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then(setDepartments)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <>
      <section className="nba-hero">
        <div className="nba-hero-inner">
          <span className="nba-kicker">StaffSync HRMS</span>
          <h1 className="nba-title">Departments</h1>
          <p className="nba-subtitle">
            Every squad in the organization, all in one lineup.
          </p>
        </div>
      </section>

      <div className="nba-container">
        <div className="nba-section-head">
          <h2>All Departments</h2>
          <span className="nba-count">{departments.length} teams</span>
        </div>

        {loading && <p className="nba-loading">Loading departments…</p>}
        {error && <p className="nba-error">Error: {error}</p>}
        {!loading && !error && departments.length === 0 && (
          <p className="nba-empty">No departments found.</p>
        )}
        {!loading && !error && departments.length > 0 && (
          <div className="nba-grid">
            {departments.map((dept) => (
              <article key={dept.id} className="nba-card">
                <span className="nba-card-id">Dept #{dept.id}</span>
                <h3 className="nba-card-name">{dept.name}</h3>
              </article>
            ))}
          </div>
        )}
      </div>
    </>
  )
}

export default Departments
