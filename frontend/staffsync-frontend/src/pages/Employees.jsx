import { useEffect, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

function Employees() {
  const [employees, setEmployees] = useState([])
  const [departments, setDepartments] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([
      fetch(`${API_URL}/api/employees/`).then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      }),
      fetch(`${API_URL}/api/departments/`).then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      }),
    ])
      .then(([employeesData, departmentsData]) => {
        setEmployees(employeesData)
        setDepartments(
          Object.fromEntries(departmentsData.map((d) => [d.id, d.name])),
        )
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <>
      <section className="nba-hero">
        <div className="nba-hero-inner">
          <span className="nba-kicker">StaffSync HRMS</span>
          <h1 className="nba-title">Employees</h1>
          <p className="nba-subtitle">
            The full roster — stats, squads and signing dates.
          </p>
        </div>
      </section>

      <div className="nba-container">
        <div className="nba-section-head">
          <h2>Full Roster</h2>
          <span className="nba-count">{employees.length} players</span>
        </div>

        {loading && <p className="nba-loading">Loading employees…</p>}
        {error && <p className="nba-error">Error: {error}</p>}
        {!loading && !error && employees.length === 0 && (
          <p className="nba-empty">No employees found.</p>
        )}
        {!loading && !error && employees.length > 0 && (
          <div className="nba-table-wrap">
            <table className="nba-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Player</th>
                  <th>Email</th>
                  <th>Team</th>
                  <th>Signed</th>
                </tr>
              </thead>
              <tbody>
                {employees.map((emp) => (
                  <tr key={emp.id}>
                    <td>{emp.id}</td>
                    <td className="nba-player">{emp.name}</td>
                    <td>{emp.email}</td>
                    <td>
                      {emp.department_id ? (
                        <span className="nba-badge">
                          {departments[emp.department_id] ??
                            `Dept #${emp.department_id}`}
                        </span>
                      ) : (
                        '—'
                      )}
                    </td>
                    <td>
                      {emp.hire_date
                        ? new Date(emp.hire_date).toLocaleDateString()
                        : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  )
}

export default Employees
