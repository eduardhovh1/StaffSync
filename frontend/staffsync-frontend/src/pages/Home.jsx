import { Link } from 'react-router-dom'

function Home() {
  return (
    <>
      <section className="nba-hero">
        <div className="nba-hero-inner">
          <span className="nba-kicker">HRMS</span>
          <h1 className="nba-title">Welcome to StaffSync</h1>
          <p className="nba-subtitle">
            Your whole organization at a glance — teams, roster and signing
            dates, all in one place.
          </p>
          <div className="nba-actions">
            <Link to="/departments" className="nba-btn">
              View Departments
            </Link>
            <Link to="/employees" className="nba-btn nba-btn-secondary">
              View Employees
            </Link>
          </div>
        </div>
      </section>

      <div className="nba-container">
        <div className="nba-section-head">
          <h2>Explore</h2>
          <span className="nba-count">2 sections</span>
        </div>

        <div className="nba-grid">
          <Link to="/departments" className="nba-card">
            <span className="nba-card-id">Section 01</span>
            <h3 className="nba-card-name">Departments</h3>
            <p className="nba-subtitle">
              Browse every squad in the organization lineup.
            </p>
          </Link>
          <Link to="/employees" className="nba-card">
            <span className="nba-card-id">Section 02</span>
            <h3 className="nba-card-name">Employees</h3>
            <p className="nba-subtitle">
              Check the full roster with teams and signing dates.
            </p>
          </Link>
        </div>
      </div>
    </>
  )
}

export default Home
