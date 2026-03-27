import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

// Request interceptor - add JWT token to all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access');
  if (token) {
    config.headers.Authorization = `JWT ${token}`;
  }
  return config;
});

// Response interceptor - handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email, password) => api.post('/api/login/', { email, password }),
  register: (data) => api.post('/api/register/', data),
  me: () => api.get('/api/user/me/'),  // Must be named 'me' for AuthContext
};

export const studentAPI = {
  getAll: () => api.get('/api/students/'),
  getMe: () => api.get('/api/students/me/'),
};

export const meetingsAPI = {
  getAll: () => api.get('/api/meetings/'),
  getById: (id) => api.get(`/api/meetings/${id}/`),
  create: (data) => api.post('/api/meetings/', data),
  join: (id) => api.post(`/api/meetings/${id}/join/`),
  findByCode: (code) => api.get(`/api/meetings/find-by-code/?code=${code}`),
};

export default api;