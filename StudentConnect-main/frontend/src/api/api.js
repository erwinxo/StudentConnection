import axios from 'axios';

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  signup: (userData) => api.post('/api/auth/signup', userData),
  login: (credentials) => api.post('/api/auth/login', credentials),
  getCurrentUser: () => api.get('/api/auth/me'),
  updateProfile: (userData) => api.put('/api/auth/profile', userData),
  updateProfilePicture: (formData) => api.post('/api/auth/profile/picture', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getUserProfile: (username) => api.get(`/api/auth/user/${username}`),
  forgotPassword: (email) => api.post('/api/auth/forgot-password', { email }),
  resetPassword: (token, newPassword) => api.post('/api/auth/reset-password', { 
    token, 
    new_password: newPassword 
  }),
};

// Posts API
export const postsAPI = {
  createPost: (formData) => api.post('/api/posts/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getPosts: (params) => api.get('/api/posts/', { params }),
  getPost: (postId) => api.get(`/api/posts/${postId}`),
  getUserPosts: (username, params) => api.get(`/api/posts/user/${username}`, { params }),
};

// Comments API
export const commentsAPI = {
  createComment: (commentData) => api.post('/api/comments/', commentData),
  getPostComments: (postId) => api.get(`/api/comments/${postId}`),
};

// Standalone exports for convenience
export const resetPassword = authAPI.resetPassword;

export default api;
