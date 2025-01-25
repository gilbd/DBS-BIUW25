import React, { useState, useEffect } from 'react';
import { Box, TextField, Button, Typography, Paper } from '@mui/material';
import { userService } from '../services/api';
import Layout from '../components/layout/Layout';

function PersonalInfo() {
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    date_of_birth: '',
    weight: '',
    height: '',
    sex: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await userService.getProfile();
        if (response.status === 'success') {
          setProfile(response.data);
        } else {
          setError(response.message || 'Failed to load profile');
        }
      } catch (err) {
        console.error('Error fetching profile:', err);
        if (err.response?.status === 401) {
          setError('Please log in to view your profile');
        } else {
          setError(err.response?.data?.message || 'Failed to load profile');
        }
      }
    };

    fetchProfile();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await userService.updateProfile(profile);
      setSuccess('Profile updated successfully');
    } catch (err) {
      setError('Failed to update profile');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <Layout>
      <Box sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5" gutterBottom>
            Personal Information
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
            <TextField
              fullWidth
              margin="normal"
              label="Name"
              name="name"
              value={profile.name}
              onChange={handleChange}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Email"
              name="email"
              type="email"
              value={profile.email}
              onChange={handleChange}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Date of Birth"
              name="date_of_birth"
              type="date"
              value={profile.date_of_birth}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Weight (kg)"
              name="weight"
              type="number"
              value={profile.weight}
              onChange={handleChange}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Height (cm)"
              name="height"
              type="number"
              value={profile.height}
              onChange={handleChange}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Sex"
              name="sex"
              select
              value={profile.sex}
              onChange={handleChange}
              SelectProps={{
                native: true,
              }}
            >
              <option value=""></option>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
            </TextField>

            {error && (
              <Typography color="error" sx={{ mt: 2 }}>
                {error}
              </Typography>
            )}
            {success && (
              <Typography color="success.main" sx={{ mt: 2 }}>
                {success}
              </Typography>
            )}

            <Button
              type="submit"
              variant="contained"
              fullWidth
              sx={{ mt: 3 }}
            >
              Update Profile
            </Button>
          </Box>
        </Paper>
      </Box>
    </Layout>
  );
}

export default PersonalInfo; 