import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Divider,
  Rating,
  Snackbar,
  Alert,
  CircularProgress,
  IconButton,
  Collapse
} from '@mui/material';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import StarIcon from '@mui/icons-material/Star';
import { ratingService } from '../services/api';

function RecipeDialog({ open, recipe, onClose, onEat }) {
  const [rating, setRating] = useState(0);
  const [message, setMessage] = useState('');
  const [severity, setSeverity] = useState('success');
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showRating, setShowRating] = useState(false);

  useEffect(() => {
    if (open && recipe) {
      console.log('Recipe in dialog:', recipe);
      setRating(0);
      setShowRating(false);
      if (recipe.is_eaten) {
        console.log('Recipe is eaten, fetching rating');
        fetchRating();
      }
    }
  }, [open, recipe]);

  if (!recipe) return null;

  // Function to format ingredients
  const formatIngredients = (ingredientsString) => {
    if (!ingredientsString) return '';
    return ingredientsString
      .split('^')
      .map((ingredient, index) => `${index + 1}. ${ingredient.trim()}`)
      .join('\n');
  };

  const fetchRating = async () => {
    try {
      setIsLoading(true);
      const response = await ratingService.getUserRating(recipe.recipe_id);
      if (response.status === 'success' && response.data) {
        setRating(response.data.rating);
      }
    } catch (error) {
      console.error('Error fetching rating:', error);
      setMessage('Failed to load rating');
      setSeverity('error');
      setShowSnackbar(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRating = async (newValue) => {
    try {
      setIsLoading(true);
      await ratingService.rateRecipe(recipe.recipe_id, newValue);
      setRating(newValue);
      setMessage('Rating saved successfully');
      setSeverity('success');
      setShowSnackbar(true);
    } catch (error) {
      setMessage(error.response?.data?.message || 'Failed to save rating');
      setSeverity('error');
      setShowSnackbar(true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
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

          {recipe?.is_eaten && (
            <Box sx={{ mt: 2 }}>
              <Button
                startIcon={<StarIcon />}
                onClick={() => setShowRating(!showRating)}
                variant="outlined"
                color="primary"
                sx={{ mb: 1 }}
                data-testid="rate-button"
              >
                {showRating ? 'Hide Rating' : 'Rate This Recipe'}
              </Button>
              
              <Collapse in={showRating}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                  <Typography component="legend">Your rating:</Typography>
                  <Rating
                    value={rating}
                    onChange={(event, newValue) => {
                      handleRating(newValue);
                    }}
                    precision={1}
                    disabled={isLoading}
                  />
                  {rating > 0 && (
                    <Typography variant="body2" color="text.secondary">
                      ({rating} stars)
                    </Typography>
                  )}
                  {isLoading && (
                    <CircularProgress size={20} sx={{ ml: 1 }} />
                  )}
                </Box>
              </Collapse>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Close</Button>
          {!recipe?.is_eaten && (
            <Button 
              onClick={() => onEat(recipe.recipe_id)}
              startIcon={<RestaurantIcon />}
              variant="contained"
              color="primary"
            >
              I ate this!
            </Button>
          )}
        </DialogActions>
      </Dialog>

      <Snackbar
        open={showSnackbar}
        autoHideDuration={6000}
        onClose={() => setShowSnackbar(false)}
      >
        <Alert severity={severity} onClose={() => setShowSnackbar(false)}>
          {message}
        </Alert>
      </Snackbar>
    </>
  );
}

export default RecipeDialog;