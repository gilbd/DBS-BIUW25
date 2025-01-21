import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Divider
} from '@mui/material';
import RestaurantIcon from '@mui/icons-material/Restaurant';

function RecipeDialog({ open, recipe, onClose, onEat }) {
  if (!recipe) return null;

  // Function to format ingredients
  const formatIngredients = (ingredientsString) => {
    if (!ingredientsString) return '';
    return ingredientsString
      .split('^')
      .map((ingredient, index) => `${index + 1}. ${ingredient.trim()}`)
      .join('\n');
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {recipe.recipe_name}
        <Typography variant="subtitle1" color="text.secondary">
          {recipe.total_time && `Cooking Time: ${recipe.total_time} minutes`}
        </Typography>
      </DialogTitle>
      <DialogContent>
        <Box sx={{ mb: 2 }}>
          <img
            src={recipe.image || 'https://via.placeholder.com/600x400'}
            alt={recipe.recipe_name}
            style={{ width: '100%', maxHeight: '400px', objectFit: 'cover' }}
          />
        </Box>
        
        <Typography variant="h6" gutterBottom>Ingredients</Typography>
        <Typography paragraph style={{ whiteSpace: 'pre-line' }}>
          {formatIngredients(recipe.ingredients)}
        </Typography>
        
        <Divider sx={{ my: 2 }} />
        
        <Typography variant="h6" gutterBottom>Directions</Typography>
        <Typography paragraph style={{ whiteSpace: 'pre-line' }}>
          {recipe.directions}
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
        <Button 
          onClick={() => onEat(recipe.recipe_id)}
          startIcon={<RestaurantIcon />}
          variant="contained"
          color="primary"
        >
          I ate this!
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default RecipeDialog;