/**
 * API client — Axios instance with auth interceptor.
 */

import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: { 'Accept': 'application/json' },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 responses globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      // Don't redirect if already on auth page
      if (!window.location.pathname.startsWith('/login') &&
          !window.location.pathname.startsWith('/register')) {
        // Only redirect protected routes
      }
    }
    return Promise.reject(error);
  }
);

// ── Auth APIs ──
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  getProfile: () => api.get('/auth/profile'),
};

// ── Analysis APIs ──
export const analysisAPI = {
  analyze: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000, // 60s for analysis
    });
  },
};

// ── History APIs ──
export const historyAPI = {
  getList: (page = 1, pageSize = 20) =>
    api.get(`/history?page=${page}&page_size=${pageSize}`),
  getDetail: (id) => api.get(`/history/${id}`),
  delete: (id) => api.delete(`/history/${id}`),
};

// ── Dashboard APIs ──
export const dashboardAPI = {
  getStats: () => api.get('/dashboard'),
};

// ── Health API ──
export const healthAPI = {
  check: () => api.get('/health'),
};

export default api;
