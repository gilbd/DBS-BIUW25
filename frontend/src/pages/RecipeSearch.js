import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Rating,
  Stack
} from '@mui/material';
import { recipeService, ratingService } from '../services/api';
import Layout from '../components/layout/Layout';
import RecipeDialog from '../components/RecipeDialog';
import { useAuth } from '../contexts/AuthContext';
import { dietService } from '../services/api';
import StarIcon from '@mui/icons-material/Star';

function RecipeSearch() {
  const [searchParams, setSearchParams] = useState({
    query: '',
    diet: '',
    maxTime: '',
    ingredient: ''
  });
  const [recipes, setRecipes] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const { user } = useAuth();
  const [diets, setDiets] = useState([]);
  const [ratings, setRatings] = useState({});

  // Fetch diets when component mounts
  useEffect(() => {
    const fetchDiets = async () => {
      try {
        const response = await dietService.getAllDiets();
        if (response.status === 'success') {
          setDiets(response.data);
        }
      } catch (error) {
        console.error('Error fetching diets:', error);
      }
    };
    fetchDiets();
  }, []);

  // Fetch rating for eaten recipes
  const fetchRating = async (recipeId) => {
    try {
      const response = await ratingService.getUserRating(recipeId);
      if (response.status === 'success' && response.data) {
        setRatings(prev => ({
          ...prev,
          [recipeId]: response.data.rating
        }));
      }
    } catch (error) {
      console.error('Error fetching rating:', error);
    }
  };

  // Fetch ratings when recipes change
  useEffect(() => {
    recipes.forEach(recipe => {
      if (recipe.is_eaten) {
        fetchRating(recipe.recipe_id);
      }
    });
  }, [recipes]);

  const handleSearch = async () => {
    try {
      // Only send non-empty parameters
      const filteredParams = Object.fromEntries(
        Object.entries(searchParams).filter(([_, value]) => value !== '')
      );
      
      const response = await recipeService.searchRecipes(filteredParams);
      if (response.status === 'success' && Array.isArray(response.data)) {
        setRecipes(response.data);
      }
    } catch (error) {
      console.error('Error searching recipes:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleRecipeClick = async (recipeId) => {
    try {
      const recipeData = await recipeService.getRecipeById(recipeId);
      console.log('Recipe data:', recipeData); // Debug log
      setSelectedRecipe(recipeData);
      setDialogOpen(true);
    } catch (error) {
      console.error('Error fetching recipe:', error);
    }
  };

  const handleEatRecipe = async (recipeId) => {
    try {
      if (!user) {
        console.error('User not logged in');
        return;
      }
      
      await recipeService.logEatenRecipe(user.user_id, recipeId);
      setDialogOpen(false);
      setSelectedRecipe(null);
      
      // Refresh the search results to update the eaten status
      handleSearch();
    } catch (error) {
      console.error('Error logging eaten recipe:', error);
    }
  };

  const handleRating = async (recipeId, newValue) => {
    try {
      await ratingService.rateRecipe(recipeId, newValue);
      setRatings(prev => ({
        ...prev,
        [recipeId]: newValue
      }));
    } catch (error) {
      console.error('Error saving rating:', error);
    }
  };

  return (
    <Layout>
      <Box sx={{ maxWidth: 1200, mx: 'auto', mt: 4 }}>
        <Grid container spacing={2} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Search Recipes"
              name="query"
              value={searchParams.query}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Diet</InputLabel>
              <Select
                name="diet"
                value={searchParams.diet}
                onChange={handleChange}
                label="Diet"
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="dairy_free">Dairy Free</MenuItem>
                <MenuItem value="egg_allergy">Egg Allergy</MenuItem>
                <MenuItem value="gluten_free">Gluten Free</MenuItem>
                <MenuItem value="nut_allergy">Nut Allergy</MenuItem>
                <MenuItem value="shellfish_allergy">Shellfish Allergy</MenuItem>
                <MenuItem value="vegan">Vegan</MenuItem>
                <MenuItem value="vegetarian">Vegetarian</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Max Cooking Time (minutes)"
              name="maxTime"
              type="number"
              value={searchParams.maxTime}
              onChange={handleChange}
              InputProps={{ inputProps: { min: 0 } }}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Main Ingredient"
              name="ingredient"
              value={searchParams.ingredient}
              onChange={handleChange}
            />
          </Grid>
        </Grid>

        <Button
          variant="contained"
          onClick={handleSearch}
          sx={{ mb: 4 }}
        >
          Search
        </Button>

        <Grid container spacing={3}>
          {recipes.map((recipe) => (
            <Grid item xs={12} sm={6} md={3} key={recipe.recipe_id}>
              <Card 
                sx={{ 
                  cursor: 'pointer',
                  backgroundColor: recipe.is_eaten ? '#e8f5e9' : 'white',
                  '&:hover': {
                    transform: 'scale(1.02)',
                    transition: 'transform 0.2s ease-in-out'
                  }
                }}
                onClick={() => handleRecipeClick(recipe.recipe_id)}
              >
                <CardMedia
                  component="img"
                  height="140"
                  image={recipe.image || 'https://via.placeholder.com/300x200'}
                  alt={recipe.recipe_name}
                />
                <CardContent>
                  <Typography gutterBottom variant="h6">
                    {recipe.recipe_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Time: {recipe.total_time} minutes
                  </Typography>
                  {recipe.is_eaten && (
                    <Stack direction="row" alignItems="center" spacing={1} sx={{ mt: 1 }}>
                      <Typography component="legend" variant="body2">
                        Your Rating:
                      </Typography>
                      <Rating
                        value={ratings[recipe.recipe_id] || 0}
                        onChange={(event, newValue) => {
                          event.stopPropagation();
                          handleRating(recipe.recipe_id, newValue);
                        }}
                        onClick={(e) => e.stopPropagation()}
                        size="small"
                      />
                    </Stack>
                  )}
                  {recipe.diets?.length > 0 && (
                    <Box sx={{ mt: 1, mb: 1 }}>
                      {recipe.diets.map((diet) => (
                        <Chip
                          key={diet}
                          label={diet}
                          size="small"
                          sx={{ mr: 0.5, mb: 0.5 }}
                        />
                      ))}
                    </Box>
                  )}
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {recipe.ingredients && recipe.ingredients.split('^')
                      .slice(0, 2)
                      .map((ingredient, index) => `${index + 1}. ${ingredient.trim()}`)
                      .join('\n')}
                    ...
                  </Typography>
                </CardContent>
              </Card>
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

export default RecipeSearch; 