import React, { useState, useEffect, useContext } from 'react';
import { Box, Typography, Grid, Card, CardContent, CardMedia } from '@mui/material';
import { recipeService } from '../services/api';
import Layout from '../components/layout/Layout';
import RecipeDialog from '../components/RecipeDialog';
import { useAuth } from '../contexts/AuthContext';

function MainPage() {
  const [recentRecipes, setRecentRecipes] = useState([]);
  const [recommendedRecipes, setRecommendedRecipes] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      fetchData();
    }
  }, [user]);

  const fetchData = async () => {
    try {
      // Fetch recommendations
      const recommendationsResponse = await recipeService.getRecommendations(user?.user_id);
      if (recommendationsResponse.status === 'success' && Array.isArray(recommendationsResponse.data)) {
        setRecommendedRecipes(recommendationsResponse.data.slice(0, 3));
      }

      // Fetch recent recipes
      const recentResponse = await recipeService.getRecentRecipes(user?.user_id);
      if (recentResponse.status === 'success' && Array.isArray(recentResponse.data)) {
        setRecentRecipes(recentResponse.data);
      }
    } catch (error) {
      console.error('Error fetching recipes:', error);
    }
  };

  const handleRecipeClick = (recipe) => {
    setSelectedRecipe(recipe);
    setDialogOpen(true);
  };

  const handleEatRecipe = async (recipeId) => {
    try {
      if (!user) {
        console.error('User not logged in');
        return;
      }
      
      await recipeService.logEatenRecipe(user.user_id, recipeId);
      setDialogOpen(false);  // Close the dialog first
      setSelectedRecipe(null);  // Clear the selected recipe
      
      // Get a new uneaten recipe to replace the eaten one
      const response = await recipeService.getNewRecommendation(user.user_id);
      if (response.status === 'success' && response.data) {
        // Update recommendedRecipes by replacing the eaten recipe with the new one
        setRecommendedRecipes(prevRecipes => 
          prevRecipes.map(recipe => 
            recipe.recipe_id === recipeId ? response.data : recipe
          )
        );
      }

      // Refresh recent recipes to include the newly eaten recipe
      const recentResponse = await recipeService.getRecentRecipes(user.user_id);
      if (recentResponse.status === 'success' && Array.isArray(recentResponse.data)) {
        setRecentRecipes(recentResponse.data);
      }
    } catch (error) {
      console.error('Error logging eaten recipe:', error);
    }
  };

  const RecipeCard = ({ recipe }) => {
    // Function to format ingredients
    const formatIngredients = (ingredientsString) => {
      if (!ingredientsString) return '';
      return ingredientsString
        .split('^')
        .map((ingredient, index) => `${index + 1}. ${ingredient.trim()}`)
        .slice(0, 2) // Show only first 2 ingredients in the card
        .join('\n');
    };

    return (
      <Card 
        sx={{ 
          height: '100%', 
          display: 'flex', 
          flexDirection: 'column',
          cursor: 'pointer',
          backgroundColor: recipe.is_eaten ? '#e8f5e9' : 'white',
          '&:hover': {
            transform: 'scale(1.02)',
            transition: 'transform 0.2s ease-in-out'
          }
        }}
        onClick={() => handleRecipeClick(recipe)}
      >
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
            {formatIngredients(recipe.ingredients)}...
          </Typography>
        </CardContent>
      </Card>
    );
  };

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

        <RecipeDialog
          open={dialogOpen}
          recipe={selectedRecipe}
          onClose={() => setDialogOpen(false)}
          onEat={handleEatRecipe}
        />
      </Box>
    </Layout>
  );
}

export default MainPage; 