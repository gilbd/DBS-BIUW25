# Recipe Recommendation App - Development Guide

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm (v6 or higher)
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment files:
```bash
# .env.development
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development

# .env.production
REACT_APP_API_URL=https://api.yourapp.com
REACT_APP_ENV=production
```


## Development Workflow

### Running the Application
```bash
# Development mode
npm start
# Production build
npm run build
# Run tests
npm test
```

### Code Structure Guidelines

#### Components
- Place reusable components in `src/components`
- Use functional components with hooks
- Follow naming convention: PascalCase
- Create component-specific styles using MUI's `sx` prop

#### Pages
- Place page components in `src/pages`
- Include route configuration in `App.js`
- Implement proper loading and error states

#### API Integration
- Add API endpoints in `services/api.js`
- Use try-catch for error handling
- Implement proper loading states
- Handle token refresh/expiration

## Testing

### Unit Tests
```bash
# Run all tests
npm test
# Run specific test
npm test -- -t "test-name"
# Coverage report
npm test -- --coverage
```

### E2E Tests (if implemented)
```bash
# Run Cypress tests
npm run cypress:open
```


## Build and Deployment

### Development Build
```bash
npm start
```


### Production Build
```bash
npm run build
```


### Deployment
1. Create production build
2. Configure environment variables
3. Deploy to hosting service

## Common Tasks

### Adding New Features
1. Create necessary components
2. Add API integration
3. Update routes if needed
4. Add tests
5. Update documentation

### Troubleshooting

#### Common Issues
1. API Connection Issues
   - Check API URL in .env
   - Verify backend status
   - Check network tab for errors

2. Build Problems
   - Clear npm cache
   - Delete node_modules
   - Reinstall dependencies

3. Authentication Issues
   - Check token expiration
   - Verify API endpoints
   - Clear local storage

## Best Practices

### Code Style
- Use ESLint configuration
- Follow existing patterns
- Document complex logic
- Use TypeScript types/interfaces

### Performance
- Implement proper memoization
- Optimize images
- Lazy load routes
- Monitor bundle size

### Security
- Validate user input
- Sanitize data
- Use HTTPS
- Implement proper CORS

## Contributing
1. Create feature branch
2. Make changes
3. Write tests
4. Submit pull request
5. Wait for review

## Resources
- [React Documentation](https://reactjs.org/)
- [Material-UI Documentation](https://mui.com/)
- [React Router Documentation](https://reactrouter.com/)