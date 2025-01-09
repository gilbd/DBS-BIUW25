import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
});

// Request interceptor for adding auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: async (credentials) => {
    // credentials can have either {email, password} or {userId, password}
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },
  verify: async () => {
    const response = await api.get('/auth/verify');
    return response.data;
  }
};

export const recipeService = {
  getRecommendations: async () => {
    const response = await api.get('/recipes/recommendations');
    return response.data;
  },
  searchRecipes: async (params) => {
    const response = await api.get('/recipes/search', { params });
    return response.data;
  },
  getRecipeById: async (id) => {
    const response = await api.get(`/recipes/${id}`);
    return response.data;
  }
};

export const userService = {
  updateProfile: async (data) => {
    const response = await api.put('/users/profile', data);
    return response.data;
  },
  getProfile: async () => {
    const response = await api.get('/users/profile');
    return response.data;
  }
};

export default api; 