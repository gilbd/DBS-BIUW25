# Recipe Recommendation Frontend - Architecture Documentation

## Overview
The frontend is a React-based single-page application (SPA) that provides an intuitive interface for recipe discovery, management, and interaction. It follows component-based architecture with clear separation of concerns.

## Directory Structure
```
frontend/
├── public/                # Static files
│   ├── index.html
│   ├── manifest.json
│   └── assets/
├── src/                   # Source code
│   ├── components/        # Reusable UI components
│   │   ├── layout/
│   │   │   ├── Layout.js
│   │   │   ├── Navbar.js
│   │   │   └── Footer.js
│   │   ├── RecipeDialog.js
│   │   ├── RatingModal.js
│   │   └── common/
│   ├── pages/            # Page components
│   │   ├── MainPage.js
│   │   ├── RecipeSearch.js
│   │   ├── LoginPage.js
│   │   └── ProfilePage.js
│   ├── services/         # API services
│   │   ├── api.js
│   │   └── auth.js
│   ├── contexts/         # React contexts
│   │   └── AuthContext.js
│   ├── hooks/            # Custom hooks
│   ├── utils/            # Helper functions
│   └── App.js            # Root component
├── .env.development      # Development environment variables
└── package.json          # Project dependencies
```

## Core Components

### 1. Pages
- **MainPage**: Dashboard with recommendations and recent recipes
- **RecipeSearch**: Advanced recipe search with filters
- **LoginPage**: User authentication
- **ProfilePage**: User preferences and settings

### 2. Components
- **RecipeDialog**: Detailed recipe view with nutrition info
- **RatingModal**: Recipe rating interface
- **Layout**: Page structure with navigation
- **Common Components**: Reusable UI elements

### 3. Services
- **API Service**: 
  - Recipe operations (search, fetch, rate)
  - User operations
  - Authentication
- **Auth Service**: Token management and auth state

## Key Features

### Recipe Management
- Recipe search with multiple filters
- Detailed recipe view with nutrition information
- Recipe rating system
- Mark recipes as eaten
- Recent recipes tracking

### User Features
- JWT-based authentication
- User preferences
- Dietary restrictions
- Rating history
- Eaten recipes history

## State Management

### Context API
- **AuthContext**: User authentication state
- **ThemeContext**: UI theme preferences

### Local State
- Component-level state using useState
- Form state management
- UI state (modals, loading states)

## API Integration

### Endpoints
- Recipe operations
  ```javascript
  recipeService.searchRecipes(params)
  recipeService.getRecipeById(id)
  recipeService.getRecentRecipes(userId)
  recipeService.getRecommendations(userId)
  ```
- Rating operations
  ```javascript
  ratingService.rateRecipe(recipeId, rating)
  ratingService.getUserRating(recipeId)
  ratingService.getAverageRating(recipeId)
  ```
- Authentication
  ```javascript
  authService.login(credentials)
  authService.verify()
  ```

## Performance Optimizations
- Lazy loading of components
- Optimized recipe fetching
  - Minimal data for lists
  - Detailed data on demand
- Image optimization
- Caching strategies
- Debounced search

## UI/UX Features
- Responsive design
- Material-UI components
- Loading states
- Error handling
- Toast notifications
- Modal dialogs
- Form validation

## Security Measures
- JWT token management
- Protected routes
- Input validation
- Secure API calls
- Environment variables

## Error Handling
- API error handling
- User-friendly error messages
- Loading states
- Fallback UI components

## Technical Stack
- React 18
- Material-UI
- Axios
- React Router
- JWT Authentication

## Development Configuration
```javascript
// .env.development
REACT_APP_API_URL=http://127.0.0.1:5000/api
REACT_APP_ENV=development
```

## Testing
- Unit tests for components
- Integration tests
- API mocking
- Test utilities

## Build & Deployment
- Development server
- Production build
- Environment configuration
- Static file serving

## Future Considerations
- State management scaling
- Performance monitoring
- Analytics integration
- Progressive Web App features
- Accessibility improvements