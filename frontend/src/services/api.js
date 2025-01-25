import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',  // Use a direct URL instead of proxy
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling auth errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login if unauthorized
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (credentials) => {
    try {
      const response = await api.post('/auth/login', credentials);
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },
  verify: async () => {
    const response = await api.get('/auth/verify');
    return response.data;
  }
};

export const recipeService = {
  getRecommendations: async (userId) => {
    const response = await api.get('/recipes/recommendations', {
      params: { user_id: userId }
    });
    return response.data;
  },
  searchRecipes: async (params) => {
    const response = await api.get('/recipes/search', { params });
    return response.data;
  },
  getRecipeById: async (id) => {
    try {
      const userId = localStorage.getItem('userId');
      const response = await api.get(`/recipes/${id}`, {
        params: { user_id: userId }
      });
      console.log('Recipe response:', response.data); // For debugging
      if (response.data.status === 'success') {
        return response.data.data;
      }
      throw new Error(response.data.message || 'Failed to fetch recipe');
    } catch (error) {
      console.error('Error fetching recipe:', error);
      throw error;
    }
  },
  logEatenRecipe: async (userId, recipeId) => {
    const response = await api.post('/eats/eats', {
      user_id: userId,
      recipe_id: recipeId
    });
    return response.data;
  },
  getRecentRecipes: async (userId) => {
    const response = await api.get('/recipes/recent', {
      params: { user_id: userId }
    });
    return response.data;
  },
  getNewRecommendation: async (userId) => {
    const response = await api.get('/recipes/new-recommendation', {
      params: { user_id: userId }
    });
    return response.data;
  },
};

export const userService = {
  updateProfile: async (data) => {
    try {
      const response = await api.put('/users/profile', data);
      return response.data;
    } catch (error) {
      console.error('Error updating profile:', error);
      throw error;
    }
  },
  getProfile: async () => {
    try {
      const response = await api.get('/users/profile');
      return response.data;
    } catch (error) {
      console.error('Error getting profile:', error);
      throw error;
    }
  }
};

export const dietService = {
  getAllDiets: async () => {
    const response = await api.get('/diets');
    return response.data;
  }
};

export const ratingService = {
  rateRecipe: async (recipeId, rating) => {
    try {
      const response = await api.post('/rating/rate', {
        recipe_id: recipeId,
        rating: rating
      });
      return response.data;
    } catch (error) {
      console.error('Error rating recipe:', error);
      throw error;
    }
  },
  getUserRating: async (recipeId) => {
    try {
      const response = await api.get(`/rating/user-rating/${recipeId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting user rating:', error);
      throw error;
    }
  }
};

export default api; 