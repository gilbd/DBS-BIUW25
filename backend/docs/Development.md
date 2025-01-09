# Recipe Recommendation Backend - Development Guide

## Getting Started

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)
- Virtual environment tool (venv)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in .env file:
```bash
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=recipe_db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

## Development Workflow

### Running the Application
```bash
# Run the application
python app.py
```

### Database Management
```bash
# Create database
mysql -u root -p
CREATE DATABASE recipe_db;

# Initialize tables
flask db init
flask db migrate
flask db upgrade
```

### Code Style
- Follow PEP 8 guidelines
- Use Black for formatting
- Run Flake8 for linting

```bash
# Format code
black .

# Run linter
flake8
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/
```

### Writing Tests
- Place tests in `tests/` directory
- Name test files with `test_` prefix
- Use pytest fixtures for setup
- Mock external services

## API Documentation

### Authentication
```bash
# Login
POST /api/auth/login
{
    "email": "user@example.com",
    "password": "password123"
}

# Verify token
GET /api/auth/verify
Header: Authorization: Bearer <token>
```

### Users
```bash
# Create user
POST /api/users
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
}
```

## Error Handling

### Common HTTP Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

### Error Response Format
```json
{
    "error": "Error message",
    "details": "Additional information"
}
```

## Deployment

### Production Setup
1. Set up production database
2. Configure environment variables
3. Set up WSGI server (Gunicorn)
4. Configure reverse proxy (Nginx)

### Environment Variables
```bash
# Production .env
DEBUG=False
DB_HOST=production_host
SECRET_KEY=production_secret
```

## Best Practices

### Security
- Always validate input
- Use parameterized queries
- Keep secrets in environment variables
- Implement rate limiting

### Performance
- Use database indexes
- Implement caching
- Optimize database queries
- Use connection pooling

### Code Organization
- Follow MVC pattern
- Keep controllers thin
- Use services for business logic
- Implement proper error handling

## Troubleshooting

### Common Issues
1. Database Connection
   - Check credentials
   - Verify host/port
   - Check network connectivity

2. Authentication Issues
   - Verify token expiration
   - Check secret keys
   - Validate request format

3. Performance Problems
   - Monitor query performance
   - Check database indexes
   - Review connection pooling

## Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [Python Testing Guide](https://docs.pytest.org/) 