import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

export default function Navigation() {
  const [user, setUser] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setMenuOpen(false);
    navigate('/');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo */}
        <Link to="/" className="navbar-logo">
          <span className="logo-icon">📄</span>
          <span className="logo-text">Resume Analyzer</span>
        </Link>

        {/* Hamburger Menu Button */}
        <button
          className={`hamburger ${menuOpen ? 'active' : ''}`}
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        {/* Navigation Menu */}
        <div className={`navbar-menu ${menuOpen ? 'active' : ''}`}>
          <div className="navbar-nav">
            {/* Main Navigation */}
            <div className="nav-section">
              <h4 className="nav-section-title">Main</h4>
              <Link
                to="/"
                className={`nav-item ${isActive('/') ? 'active' : ''}`}
                onClick={() => setMenuOpen(false)}
              >
                <span className="nav-icon">🏠</span>
                <span>Home</span>
              </Link>
              <Link
                to="/review"
                className={`nav-item ${isActive('/review') ? 'active' : ''}`}
                onClick={() => setMenuOpen(false)}
              >
                <span className="nav-icon">📊</span>
                <span>Analyze Resume</span>
              </Link>
              <Link
                to="/templates"
                className={`nav-item ${isActive('/templates') ? 'active' : ''}`}
                onClick={() => setMenuOpen(false)}
              >
                <span className="nav-icon">📋</span>
                <span>Templates</span>
              </Link>
            </div>

            {/* Authentication Section */}
            <div className="nav-section">
              <h4 className="nav-section-title">Account</h4>
              {user ? (
                <>
                  <div className="user-info">
                    <div className="user-avatar">👤</div>
                    <div>
                      <div className="user-name">{user.name}</div>
                      <div className="user-email">{user.email}</div>
                    </div>
                  </div>
                  <button
                    className="nav-item logout-btn"
                    onClick={handleLogout}
                  >
                    <span className="nav-icon">🚪</span>
                    <span>Logout</span>
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className={`nav-item ${isActive('/login') ? 'active' : ''}`}
                    onClick={() => setMenuOpen(false)}
                  >
                    <span className="nav-icon">🔐</span>
                    <span>Login</span>
                  </Link>
                  <Link
                    to="/signup"
                    className={`nav-item nav-item-signup ${isActive('/signup') ? 'active' : ''}`}
                    onClick={() => setMenuOpen(false)}
                  >
                    <span className="nav-icon">✍️</span>
                    <span>Sign Up</span>
                  </Link>
                </>
              )}
            </div>

            {/* Help Section */}
            <div className="nav-section">
              <h4 className="nav-section-title">Help</h4>
              <a
                href="#about"
                className="nav-item"
                onClick={() => setMenuOpen(false)}
              >
                <span className="nav-icon">ℹ️</span>
                <span>About</span>
              </a>
              <a
                href="#contact"
                className="nav-item"
                onClick={() => setMenuOpen(false)}
              >
                <span className="nav-icon">💬</span>
                <span>Contact</span>
              </a>
            </div>
          </div>
        </div>

        {/* Desktop Auth Buttons */}
        <div className="navbar-auth">
          {user ? (
            <div className="user-menu-desktop">
              <span className="user-greeting">Hello, {user.name}!</span>
              <button className="btn logout-btn" onClick={handleLogout}>
                Logout
              </button>
            </div>
          ) : (
            <div className="auth-links">
              <Link to="/login" className="btn auth-btn">
                Login
              </Link>
              <Link to="/signup" className="btn primary auth-btn">
                Sign Up
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
