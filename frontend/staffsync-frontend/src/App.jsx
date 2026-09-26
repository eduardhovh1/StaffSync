import { Route, Routes } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Departments from './pages/Departments.jsx'
import Employees from './pages/Employees.jsx'
import Home from './pages/Home.jsx'

function App() {
  return (
    <>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/departments" element={<Departments />} />
          <Route path="/employees" element={<Employees />} />
          <Route
            path="*"
            element={<p className="nba-empty">404 — Page not found.</p>}
          />
        </Routes>
      </main>
      <footer className="nba-footer">StaffSync HRMS — Built for the team</footer>
    </>
  )
}

export default App
