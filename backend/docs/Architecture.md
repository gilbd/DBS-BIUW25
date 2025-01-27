# Recipe Recommendation Backend - Architecture Documentation

## Overview
The Recipe Recommendation Backend is a Flask-based REST API that provides recipe management, user authentication, and recommendation services. The application follows a modular architecture with clear separation of concerns and domain-driven design principles.

## Directory Structure
```
backend/
├── app.py                  # Application entry point
├── config/                 # Configuration files
│   ├── __init__.py
│   ├── database.py        # Database configuration
│   └── settings.py        # Application settings
├── controllers/           # Route handlers and business logic
│   ├── __init__.py
│   ├── admin_controller.py
│   ├── auth_controller.py
│   ├── contains_controller.py
│   ├── diet_controller.py
│   ├── fits_controller.py
│   ├── nutrition_controller.py
│   ├── rating_controller.py
│   ├── recipe_controller.py
│   ├── user_controller.py
│   └── user_diet_controller.py
├── models/               # Database models
│   ├── __init__.py
│   ├── diet.py
│   ├── nutrition.py
│   ├── recipe.py
│   ├── user.py
│   └── relationships/
│       ├── contains.py
│       ├── eats.py
│       ├── fits.py
│       ├── rates.py
│       └── user_diet.py
├── utils/               # Helper functions
│   ├── __init__.py
│   └── auth.py         # Authentication utilities
├── docs/               # Documentation
├── requirements.txt    # Project dependencies
└── .env               # Environment variables
```

## Core Components

### 1. Models
- **Recipe**: Core recipe information including ingredients and directions
- **Nutrition**: Nutritional information with units and daily values
- **Diet**: Dietary categories and restrictions
- **User**: User account information
- **Relationship Models**:
  - Contains: Links recipes to nutrition information
  - Fits: Maps recipes to compatible diets
  - Eats: Tracks user's eaten recipes
  - Rates: Stores user ratings for recipes
  - UserDiet: Associates users with their dietary preferences

### 2. Controllers
- **Recipe Controller**: 
  - Recipe CRUD operations
  - Recipe search and filtering
  - Recommendations
  - Recent recipes
- **Nutrition Controller**: Manage nutritional information
- **Diet Controller**: Diet management and assignment
- **Rating Controller**: Recipe rating system
- **User Diet Controller**: User dietary preferences
- **Contains Controller**: Recipe nutrition management
- **Fits Controller**: Diet-recipe associations

### 3. API Endpoints

#### Recipe Endpoints
- GET /api/recipes/<id> - Get recipe details with nutrition
- GET /api/recipes/search - Search recipes with filters
- GET /api/recipes/recommendations - Get personalized recommendations
- GET /api/recipes/recent - Get recently eaten recipes
- POST /api/recipes - Create new recipe
- PUT /api/recipes/<id> - Update recipe
- DELETE /api/recipes/<id> - Delete recipe

#### Nutrition & Diet Endpoints
- GET /api/nutrition - Get all nutrition items
- POST /api/contains - Add nutrition to recipe
- GET /api/diets - Get all diets
- POST /api/fits - Assign recipe to diet
- POST /api/user_diets - Assign diet to user

#### Rating Endpoints
- POST /api/rating/rate - Rate a recipe
- GET /api/rating/user-rating/<recipe_id> - Get user's rating
- GET /api/rating/average/<recipe_id> - Get average rating

## Data Models

### Recipe
- recipe_id (PK)
- recipe_name
- total_time
- image
- directions
- ingredients

### Nutrition
- name (PK)
- unit
- average_daily_value

### Diet
- diet_id (PK)
- name
- keywords
- description

### Relationships
- Contains (recipe_id, nutrition_name, amount)
- Fits (recipe_id, diet_id)
- UserDiet (user_id, diet_id)
- Eats (user_id, recipe_id, created_at)
- Rates (user_id, recipe_id, rating)

## Performance Optimizations
- Optimized recipe queries with minimal joins
- Separate endpoints for basic and detailed recipe information
- Efficient nutrition data retrieval
- Caching for frequently accessed data
- Pagination for large result sets

## Security Measures
- Input validation
- SQL injection prevention
- Authentication required for sensitive operations
- Rate limiting
- CORS protection

## Error Handling
- Standardized error responses
- Detailed logging
- Graceful failure handling
- User-friendly error messages

## Technical Stack

### Framework
- Flask 3.0.0
- Flask-SQLAlchemy
- Flask-CORS
- PyJWT

### Database
- MySQL
- SQLAlchemy ORM
- PyMySQL driver

### Security
- JWT tokens
- Password hashing
- CORS protection
- Input validation

## API Structure

### Authentication Endpoints
- POST /api/auth/login
- GET /api/auth/verify

### Recipe Endpoints
- GET /api/recipes
- POST /api/recipes
- GET /api/recipes/<id>
- PUT /api/recipes/<id>
- DELETE /api/recipes/<id>

### User Endpoints
- GET /api/users
- POST /api/users
- GET /api/users/<id>
- PUT /api/users/<id>
- DELETE /api/users/<id>

### Admin Endpoints
- GET /api/admin/stats
- GET /api/admin/users
- GET /api/admin/recipes

## Security Measures

### 1. Authentication
- JWT token validation
- Token expiration
- Secure password storage

### 2. Authorization
- Role-based access control
- Route protection
- Resource ownership validation

### 3. Data Protection
- Input sanitization
- SQL injection prevention
- XSS protection

## Error Handling
- Standardized error responses
- HTTP status codes
- Detailed error messages
- Error logging

## Performance Considerations
- Database indexing
- Query optimization
- Connection pooling
- Response caching 
