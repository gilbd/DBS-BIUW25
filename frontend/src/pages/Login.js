import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Tabs,
  Tab,
  Alert,
} from '@mui/material';

function Login() {
  const [loginMethod, setLoginMethod] = useState('email');
  const [email, setEmail] = useState('');
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleTabChange = (event, newValue) => {
    setLoginMethod(newValue);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (loginMethod === 'email') {
        await login({ email, password });
      } else {
        await login({ userId: parseInt(userId), password });
      }
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to login');
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <Typography component="h1" variant="h5" align="center" gutterBottom>
            Recipe Recommendation App
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mt: 2, width: '100%' }}>
              {error}
            </Alert>
          )}

          <Tabs
            value={loginMethod}
            onChange={handleTabChange}
            centered
            sx={{ mb: 3 }}
          >
            <Tab label="Email" value="email" />
            <Tab label="User ID" value="userId" />
          </Tabs>

          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
            {loginMethod === 'email' ? (
              <TextField
                margin="normal"
                required
                fullWidth
                label="Email Address"
                autoComplete="email"
                autoFocus
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            ) : (
              <TextField
                margin="normal"
                required
                fullWidth
                label="User ID"
                type="number"
                autoFocus
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
              />
            )}

            <TextField
              margin="normal"
              required
              fullWidth
              label="Password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
          </Box>
        </Paper>

        {/* Development Hints */}
        <Paper 
          elevation={0} 
          sx={{ 
            mt: 2, 
            p: 2, 
            bgcolor: '#f5f5f5', 
            width: '100%',
            borderRadius: 1
          }}
        >
          <Typography variant="body2" color="text.secondary" align="center" sx={{ fontFamily: 'monospace' }}>
            Development Login Credentials:
            {loginMethod === 'email' ? (
              <>
                <br />User: 1972959@example.com / 123456
                <br />Admin: 12657644@example.com / 123456
              </>
            ) : (
              <>
                <br />User: 1972959 / 123456
                <br />Admin: 12657644 / 123456
              </>
            )}
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
}

export default Login; 