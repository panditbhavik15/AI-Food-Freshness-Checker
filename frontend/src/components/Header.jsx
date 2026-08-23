/**
 * Header component — navigation, auth status, mobile menu.
 */

import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import './Header.css';

export default function Header() {
  const { user, isAuthenticated, logout } = useAuth();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  return (
    <header className="header">
      <div className="header__inner container">
        <Link to="/" className="header__logo" id="nav-logo">
          <span className="header__logo-icon">🍃</span>
          <span className="header__logo-text">
            Fresh<span className="gradient-text">Check</span>
          </span>
        </Link>

        <nav className={`header__nav ${mobileOpen ? 'header__nav--open' : ''}`}>
          <Link
            to="/"
            className={`header__link ${isActive('/') ? 'header__link--active' : ''}`}
            onClick={() => setMobileOpen(false)}
          >
            Home
          </Link>
          <Link
            to="/analyze"
            className={`header__link ${isActive('/analyze') ? 'header__link--active' : ''}`}
            onClick={() => setMobileOpen(false)}
          >
            Check Food
          </Link>
          {isAuthenticated && (
            <>
              <Link
                to="/history"
                className={`header__link ${isActive('/history') ? 'header__link--active' : ''}`}
                onClick={() => setMobileOpen(false)}
              >
                History
              </Link>
              <Link
                to="/dashboard"
                className={`header__link ${isActive('/dashboard') ? 'header__link--active' : ''}`}
                onClick={() => setMobileOpen(false)}
              >
                Dashboard
              </Link>
            </>
          )}
        </nav>

        <div className="header__actions">
          {isAuthenticated ? (
            <div className="header__user">
              <Link to="/profile" className="header__avatar" id="nav-profile">
                {(user?.display_name || user?.email || '?')[0].toUpperCase()}
              </Link>
              <button className="btn btn--secondary header__logout" onClick={logout} id="nav-logout">
                Logout
              </button>
            </div>
          ) : (
            <div className="header__auth-buttons">
              <Link to="/login" className="btn btn--secondary" id="nav-login">
                Log In
              </Link>
              <Link to="/register" className="btn btn--primary" id="nav-register">
                Sign Up
              </Link>
            </div>
          )}
          <button
            className="header__mobile-toggle"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle navigation"
          >
            <span className={`hamburger ${mobileOpen ? 'hamburger--open' : ''}`}>
              <span></span><span></span><span></span>
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}
