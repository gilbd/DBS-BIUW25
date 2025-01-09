import React, { useState, useEffect } from 'react';
import { Box, Typography, Grid, Card, CardContent, CardMedia, Rating } from '@mui/material';
import { recipeService } from '../services/api';
import Layout from '../components/layout/Layout';

function MainPage() {
  const [recentRecipes, setRecentRecipes] = useState([]);
  const [recommendedRecipes, setRecommendedRecipes] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const recommendations = await recipeService.getRecommendations();
        setRecommendedRecipes(recommendations.slice(0, 3));
        // In a real app, you'd have a separate endpoint for recent recipes
        setRecentRecipes(recommendations.slice(3, 6));
      } catch (error) {
        console.error('Error fetching recipes:', error);
      }
    };

    fetchData();
  }, []);

  const RecipeCard = ({ recipe }) => (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardMedia
        component="img"
        height="140"
        image={recipe.image || 'https://via.placeholder.com/300x200'}
        alt={recipe.recipe_name}
      />
      <CardContent>
        <Typography gutterBottom variant="h6" component="div">
          {recipe.recipe_name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Time to cook: {recipe.total_time} minutes
        </Typography>
        <Rating value={recipe.rating || 0} readOnly />
      </CardContent>
    </Card>
  );

  return (
    <Layout>
      <Box sx={{ flexGrow: 1 }}>
        <Typography variant="h4" gutterBottom>
          Recently Eaten
        </Typography>
        <Grid container spacing={3} sx={{ mb: 4 }}>
          {recentRecipes.map((recipe) => (
            <Grid item xs={12} sm={6} md={4} key={recipe.recipe_id}>
              <RecipeCard recipe={recipe} />
            </Grid>
          ))}
        </Grid>

        <Typography variant="h4" gutterBottom>
          Recommended for You
        </Typography>
        <Grid container spacing={3}>
          {recommendedRecipes.map((recipe) => (
            <Grid item xs={12} sm={6} md={4} key={recipe.recipe_id}>
              <RecipeCard recipe={recipe} />
            </Grid>
          ))}
        </Grid>
      </Box>
    </Layout>
  );
}

export default MainPage; 