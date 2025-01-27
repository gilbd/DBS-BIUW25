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
  Alert,
  ToggleButton,
  ToggleButtonGroup,
  Link,
  CircularProgress
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
import { adminService } from '../services/api';
import { useNavigate } from 'react-router-dom';

function AdminDashboard() {
  const [weeklyStats, setWeeklyStats] = useState([]);
  const [topRecipes, setTopRecipes] = useState([]);
  const [dietViolations, setDietViolations] = useState([]);
  const [calorieViolations, setCalorieViolations] = useState([]);
  const [error, setError] = useState('');
  const [topRated, setTopRated] = useState([]);
  const [ratingPeriod, setRatingPeriod] = useState('all');
  const [isTopRatedLoading, setIsTopRatedLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetching admin statistics...');
        setIsTopRatedLoading(true);  // Start loading
        setTopRated([]); // Clear existing data
        
        // Fetch all data in parallel
        const [
          weeklyResponse,
          topRecipesResponse,
          violationsResponse,
          calorieResponse,
          topRatedResponse
        ] = await Promise.all([
          adminService.getWeeklyStats(),
          adminService.getTopRecipes(),
          adminService.getDietViolations(),
          adminService.getCalorieViolations(),
          adminService.getTopRated(ratingPeriod)
        ]);

        // Set states based on responses
        if (weeklyResponse.status === 'success') {
          setWeeklyStats(weeklyResponse.data);
        }

        if (topRecipesResponse.status === 'success') {
          setTopRecipes(topRecipesResponse.data);
        }

        if (violationsResponse.status === 'success') {
          setDietViolations(violationsResponse.data);
        }

        if (calorieResponse.status === 'success') {
          setCalorieViolations(calorieResponse.data);
        }

        if (topRatedResponse.status === 'success') {
          setTopRated(topRatedResponse.data);
        }

      } catch (err) {
        console.error('Error details:', {
          message: err.message,
          response: err.response?.data,
          status: err.response?.status,
          headers: err.response?.headers
        });
        setError(err.response?.data?.message || 'Failed to fetch admin statistics');
      } finally {
        setIsTopRatedLoading(false);  // End loading
      }
    };

    fetchData();
  }, [ratingPeriod]);

  const handlePeriodChange = (event, newPeriod) => {
    if (newPeriod !== null) {
      setRatingPeriod(newPeriod);
    }
  };

  const handleRecipeClick = (recipeId) => {
    navigate(`/recipe/${recipeId}`);
  };

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
                      <TableCell>User ID</TableCell>
                      <TableCell>User</TableCell>
                      <TableCell>Recipe</TableCell>
                      <TableCell>Diet</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {dietViolations.map((violation, index) => (
                      <TableRow key={index}>
                        <TableCell>{violation.userId}</TableCell>
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
                      <TableCell>User ID</TableCell>
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
                        <TableCell>{violation.userId}</TableCell>
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

          {/* Top Rated Recipes Table */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Top Rated Recipes
                </Typography>
                <ToggleButtonGroup
                  value={ratingPeriod}
                  exclusive
                  onChange={handlePeriodChange}
                  size="small"
                >
                  <ToggleButton value="all">
                    All Time
                  </ToggleButton>
                  <ToggleButton value="week">
                    Last Week
                  </ToggleButton>
                </ToggleButtonGroup>
              </Box>
              <TableContainer>
                {isTopRatedLoading ? (
                  <Box sx={{ 
                    display: 'flex', 
                    justifyContent: 'center', 
                    alignItems: 'center', 
                    height: 200 
                  }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Recipe ID</TableCell>
                        <TableCell>Recipe Name</TableCell>
                        <TableCell align="right">Average Rating</TableCell>
                        <TableCell align="right">Number of Ratings</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {topRated.map((recipe) => (
                        <TableRow key={recipe.recipeId}>
                          <TableCell>{recipe.recipeId}</TableCell>
                          <TableCell>
                            <Link
                              component="button"
                              onClick={() => handleRecipeClick(recipe.recipeId)}
                              sx={{ 
                                textDecoration: 'none',
                                '&:hover': {
                                  textDecoration: 'underline'
                                }
                              }}
                            >
                              {recipe.recipeName}
                            </Link>
                          </TableCell>
                          <TableCell align="right">
                            {recipe.avgRating.toFixed(2)} ⭐
                          </TableCell>
                          <TableCell align="right">
                            {recipe.ratingCount}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
              </TableContainer>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Layout>
  );
}

export default AdminDashboard; 