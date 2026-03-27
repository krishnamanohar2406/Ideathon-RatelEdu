import axios from 'axios';

// const api = axios.create({
//   baseURL: 'http://localhost:8000',
// });

// api.interceptors.request.use((config) => {
//   const token = localStorage.getItem('access');
//   if (token) {
//     config.headers.Authorization = `JWT ${token}`;
//   }
//   return config;
// });

// api.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (error.response?.status === 401) {
//       localStorage.removeItem('access');
//       window.location.href = '/login';
//     }
//     return Promise.reject(error);
//   }
// );

// export const authAPI = {
//   login: (email, password) => api.post('/auth/jwt/create/', { email, password }),
//   me: () => api.get('/auth/users/me'),
// };

// export const studentsAPI = {
//   list: () => api.get('/details/students/'),
//   create: (data) => api.post('/details/students/', data),
// };

// export const matchesAPI = {
//   list: () => api.get('/matching/matches/'),
// };

// export const meetingsAPI = {
//   list: () => api.get('/meeting/meetings/'),
// };

// export default api;





// Fix the base URL if needed
const api = axios.create({
  baseURL: 'http://localhost:8000'  // Add this if not present
});

// Update auth endpoints
export const authAPI = {
  login: (email, password) => api.post('/api/login/', { email, password }),
  register: (data) => api.post('/api/register/', data),
  getCurrentUser: () => api.get('/api/user/me/'),
  refreshToken: () => api.post('/api/token/refresh/'),
};

// Fix other endpoints
export const meetingsAPI = {
  getAll: () => api.get('/api/meetings/'),
  getById: (id) => api.get(`/api/meetings/${id}/`),
  create: (data) => api.post('/api/meetings/', data),
  join: (id) => api.post(`/api/meetings/${id}/join/`),
  findByCode: (code) => api.get(`/api/meetings/find-by-code/?code=${code}`),
};

export const studentAPI = {
  getAll: () => api.get('/api/students/'),
  getMe: () => api.get('/api/students/me/'),
};