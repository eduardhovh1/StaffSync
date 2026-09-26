import { useState } from 'react'
import { NavLink } from 'react-router-dom'

function Navbar() {
  const [open, setOpen] = useState(false)

  const close = () => setOpen(false)
  const linkClass = ({ isActive }) => (isActive ? 'active' : '')

  return (
    <header className="nba-nav">
      <div className="nba-nav-inner">
        <NavLink to="/" className="nba-brand" onClick={close}>
          <span className="nba-brand-mark" aria-hidden="true" />
          Staff<span className="accent">Sync</span>
        </NavLink>

        <button
          type="button"
          className={`nba-nav-toggle${open ? ' open' : ''}`}
          aria-expanded={open}
          aria-label={open ? 'Close menu' : 'Open menu'}
          onClick={() => setOpen((value) => !value)}
        >
          <span aria-hidden="true" />
          <span aria-hidden="true" />
          <span aria-hidden="true" />
        </button>

        <nav aria-label="Main navigation">
          <ul className={`nba-menu${open ? ' open' : ''}`}>
            <li>
              <NavLink to="/" end className={linkClass} onClick={close}>
                Home
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/departments"
                className={linkClass}
                onClick={close}
              >
                Departments
              </NavLink>
            </li>
            <li>
              <NavLink to="/employees" className={linkClass} onClick={close}>
                Employees
              </NavLink>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  )
}

export default Navbar
