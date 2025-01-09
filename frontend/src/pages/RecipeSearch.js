import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Rating,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip
} from '@mui/material';
import { recipeService } from '../services/api';
import Layout from '../components/layout/Layout';

function RecipeSearch() {
  const [searchParams, setSearchParams] = useState({
    query: '',
    diet: '',
    maxTime: '',
    ingredient: ''
  });
  const [recipes, setRecipes] = useState([]);

  const handleSearch = async () => {
    try {
      const results = await recipeService.searchRecipes(searchParams);
      setRecipes(results);
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
                <MenuItem value="vegetarian">Vegetarian</MenuItem>
                <MenuItem value="vegan">Vegan</MenuItem>
                <MenuItem value="gluten-free">Gluten Free</MenuItem>
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
            <Grid item xs={12} sm={6} md={4} key={recipe.recipe_id}>
              <Card>
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
                  <Box sx={{ mt: 1 }}>
                    {recipe.diets?.map((diet) => (
                      <Chip
                        key={diet}
                        label={diet}
                        size="small"
                        sx={{ mr: 0.5, mb: 0.5 }}
                      />
                    ))}
                  </Box>
                  <Rating value={recipe.rating || 0} readOnly />
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Layout>
  );
}

export default RecipeSearch; 