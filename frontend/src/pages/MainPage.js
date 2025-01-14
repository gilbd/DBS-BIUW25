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
        const response = await recipeService.getRecommendations();
        // Check if response has the expected structure
        if (response.status === 'success' && Array.isArray(response.data)) {
          const recipes = response.data;
          setRecommendedRecipes(recipes.slice(0, 3));
          setRecentRecipes(recipes.slice(3));
        }
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
          {recipe.total_time && `Time to cook: ${recipe.total_time} minutes`}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          {recipe.ingredients && recipe.ingredients.split('\n')[0]}...
        </Typography>
      </CardContent>
    </Card>
  );

  return (
    <Layout>
      <Box sx={{ flexGrow: 1 }}>
        <Typography variant="h4" gutterBottom>
          Recently Added
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