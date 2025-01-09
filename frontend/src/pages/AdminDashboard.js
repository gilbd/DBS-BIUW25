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
  TableRow
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

function AdminDashboard() {
  const [weeklyStats, setWeeklyStats] = useState([]);
  const [topRecipes, setTopRecipes] = useState([]);
  const [dietViolations, setDietViolations] = useState([]);

  useEffect(() => {
    // In a real app, these would be API calls
    setWeeklyStats([
      { day: 'Mon', eats: 45 },
      { day: 'Tue', eats: 52 },
      { day: 'Wed', eats: 49 },
      { day: 'Thu', eats: 63 },
      { day: 'Fri', eats: 58 },
      { day: 'Sat', eats: 48 },
      { day: 'Sun', eats: 51 }
    ]);

    setTopRecipes([
      { name: 'Spaghetti Carbonara', eats: 28 },
      { name: 'Chicken Curry', eats: 25 },
      { name: 'Caesar Salad', eats: 22 },
      { name: 'Beef Stir Fry', eats: 20 },
      { name: 'Vegetable Soup', eats: 18 }
    ]);

    setDietViolations([
      { user: 'John Doe', recipe: 'Beef Burger', diet: 'Vegetarian' },
      { user: 'Jane Smith', recipe: 'Cheese Pizza', diet: 'Vegan' },
      { user: 'Bob Wilson', recipe: 'Wheat Pasta', diet: 'Gluten-Free' }
    ]);
  }, []);

  return (
    <Layout>
      <Box sx={{ maxWidth: 1200, mx: 'auto', mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Admin Dashboard
        </Typography>

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
                Diet Violations
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
        </Grid>
      </Box>
    </Layout>
  );
}

export default AdminDashboard; 