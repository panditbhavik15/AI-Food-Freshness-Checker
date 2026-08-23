/**
 * Authentication context — manages user state, login, register, logout.
 */

import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for existing token on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      authAPI.getProfile()
        .then((res) => {
          if (res.data?.success && res.data?.data) {
            setUser(res.data.data);
          }
        })
        .catch(() => {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email, password) => {
    const res = await authAPI.login({ email, password });
    const data = res.data;
    if (data?.success && data?.data) {
      localStorage.setItem('access_token', data.data.access_token);
      localStorage.setItem('refresh_token', data.data.refresh_token);
      setUser(data.data.user);
      return { success: true };
    }
    return { success: false, error: data?.error?.message || 'Login failed.' };
  }, []);

  const register = useCallback(async (email, password, displayName) => {
    const res = await authAPI.register({ email, password, display_name: displayName });
    const data = res.data;
    if (data?.success && data?.data) {
      localStorage.setItem('access_token', data.data.access_token);
      localStorage.setItem('refresh_token', data.data.refresh_token);
      setUser(data.data.user);
      return { success: true };
    }
    return { success: false, error: data?.error?.message || 'Registration failed.' };
  }, []);

  const logout = useCallback(() => {
    authAPI.logout().catch(() => {});
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  }, []);

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
