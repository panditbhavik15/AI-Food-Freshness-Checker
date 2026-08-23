/**
 * ProfilePage — User profile and settings.
 */

import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import './ProfilePage.css';

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="profile-page">
      <div className="container">
        <h1 className="profile-page__title">
          Your <span className="gradient-text">Profile</span>
        </h1>

        <div className="profile-card glass-card animate-fade-in-up">
          <div className="profile-card__avatar">
            {(user?.display_name || user?.email || '?')[0].toUpperCase()}
          </div>

          <div className="profile-card__info">
            <div className="profile-field">
              <label>Display Name</label>
              <p>{user?.display_name || 'Not set'}</p>
            </div>
            <div className="profile-field">
              <label>Email</label>
              <p>{user?.email}</p>
            </div>
            <div className="profile-field">
              <label>Member Since</label>
              <p>{user?.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}</p>
            </div>
          </div>

          <div className="profile-card__actions">
            <button className="btn btn--secondary btn--full" onClick={handleLogout}>
              Log Out
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
