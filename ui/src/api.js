import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const login = (username, password) =>
  api.post('/auth/login', { username, password });

export const createCompany = (data) =>
  api.post('/companies', data);

export const getCompanies = () =>
  api.get('/companies');

export const getCompany = (id) =>
  api.get(`/companies/${id}`);

export const deleteCompany = (id) =>
  api.delete(`/companies/${id}`);

export default api;
