import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line
} from 'recharts';
import Layout from '../components/layout/Layout';
import axios from 'axios';

function AdminDashboard() {
  const [weeklyStats, setWeeklyStats] = useState([]);
  const [topRecipes, setTopRecipes] = useState([]);
  const [dietViolations, setDietViolations] = useState([]);
  const [calorieViolations, setCalorieViolations] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetching admin statistics...');
        
        // Fetch weekly stats
        console.log('Fetching weekly stats...');
        const weeklyResponse = await axios.get('/api/admin/stats/weekly', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        console.log('Weekly stats response:', weeklyResponse);
        if (weeklyResponse.data.status === 'success') {
          setWeeklyStats(weeklyResponse.data.data);
        }

        // Fetch top recipes
        console.log('Fetching top recipes...');
        const topRecipesResponse = await axios.get('/api/admin/stats/top-recipes', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        console.log('Top recipes response:', topRecipesResponse);
        if (topRecipesResponse.data.status === 'success') {
          setTopRecipes(topRecipesResponse.data.data);
        }

        // Fetch diet violations
        console.log('Fetching diet violations...');
        const violationsResponse = await axios.get('/api/admin/stats/diet-violations', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        console.log('Diet violations response:', violationsResponse);
        if (violationsResponse.data.status === 'success') {
          setDietViolations(violationsResponse.data.data);
        }

        // Fetch calorie violations
        console.log('Fetching calorie violations...');
        const calorieResponse = await axios.get('/api/admin/stats/calorie-violations', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        console.log('Calorie violations response:', calorieResponse);
        if (calorieResponse.data.status === 'success') {
          setCalorieViolations(calorieResponse.data.data);
        }
      } catch (err) {
        console.error('Error details:', {
          message: err.message,
          response: err.response?.data,
          status: err.response?.status,
          headers: err.response?.headers
        });
        setError(err.response?.data?.message || 'Failed to fetch admin statistics');
      }
    };

    fetchData();
  }, []);

  return (
    <Layout>
      <Box sx={{ maxWidth: 1200, mx: 'auto', mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Admin Dashboard
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3}>
          {/* Weekly Stats Chart */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Weekly Eats
              </Typography>
              <LineChart width={500} height={300} data={weeklyStats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="eats" stroke="#8884d8" />
              </LineChart>
            </Paper>
          </Grid>

          {/* Top Recipes Chart */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Top Recipes This Week
              </Typography>
              <BarChart width={500} height={300} data={topRecipes}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="eats" fill="#82ca9d" />
              </BarChart>
            </Paper>
          </Grid>

          {/* Diet Violations Table */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Recent Diet Violations
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>User</TableCell>
                      <TableCell>Recipe</TableCell>
                      <TableCell>Diet Violated</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {dietViolations.map((violation, index) => (
                      <TableRow key={index}>
                        <TableCell>{violation.user}</TableCell>
                        <TableCell>{violation.recipe}</TableCell>
                        <TableCell>{violation.diet}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          </Grid>

          {/* Calorie Violations Table */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Weekly Calorie Violations
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>User</TableCell>
                      <TableCell>Age Group</TableCell>
                      <TableCell>Sex</TableCell>
                      <TableCell align="right">Avg. Daily Calories</TableCell>
                      <TableCell align="right">Recommended</TableCell>
                      <TableCell align="right">Excess %</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {calorieViolations.map((violation, index) => (
                      <TableRow 
                        key={index}
                        sx={{ 
                          backgroundColor: 
                            violation.excessPercentage > 60 ? '#ffebee' :
                            violation.excessPercentage > 50 ? '#fff3e0' : 
                            '#fff'
                        }}
                      >
                        <TableCell>{violation.user}</TableCell>
                        <TableCell>{violation.ageGroup}</TableCell>
                        <TableCell>{violation.sex}</TableCell>
                        <TableCell align="right">
                          {Math.round(violation.avgCalories).toLocaleString()}
                        </TableCell>
                        <TableCell align="right">
                          {Math.round(violation.recommended).toLocaleString()}
                        </TableCell>
                        <TableCell 
                          align="right"
                          sx={{ 
                            color: 
                              violation.excessPercentage > 60 ? 'error.main' :
                              violation.excessPercentage > 50 ? 'warning.main' : 
                              'text.primary'
                          }}
                        >
                          +{violation.excessPercentage}%
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Layout>
  );
}

export default AdminDashboard; 