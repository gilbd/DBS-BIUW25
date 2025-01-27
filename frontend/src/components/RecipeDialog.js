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
  Snackbar,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper
} from '@mui/material';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import StarIcon from '@mui/icons-material/Star';
import { ratingService } from '../services/api';
import RatingModal from './RatingModal';

function RecipeDialog({ open, recipe, onClose, onEat }) {
  const [rating, setRating] = useState(0);
  const [averageRating, setAverageRating] = useState(null);
  const [message, setMessage] = useState('');
  const [severity, setSeverity] = useState('success');
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showRating, setShowRating] = useState(false);
  const [ratingModalOpen, setRatingModalOpen] = useState(false);

  useEffect(() => {
    if (open && recipe) {
      console.log('Dialog opened with recipe:', recipe);
      setRating(0);
      setShowRating(false);
      setAverageRating(null);
      fetchAverageRating();
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
      await fetchAverageRating();
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

  const fetchAverageRating = async () => {
    try {
      const response = await ratingService.getAverageRating(recipe.recipe_id);
      if (response.status === 'success') {
        setAverageRating(response.data);
      }
    } catch (error) {
      console.error('Error fetching average rating:', error);
    }
  };

  const handleRatingSubmit = async (newValue) => {
    try {
      setIsLoading(true);
      await ratingService.rateRecipe(recipe.recipe_id, newValue);
      setRating(newValue);
      await fetchAverageRating();
      setMessage('Rating saved successfully');
      setSeverity('success');
      setShowSnackbar(true);
      setRatingModalOpen(false);
    } catch (error) {
      setMessage(error.response?.data?.message || 'Failed to save rating');
      setSeverity('error');
      setShowSnackbar(true);
    } finally {
      setIsLoading(false);
    }
  };

  const renderNutritionTable = () => {
    // Check if nutrition_info exists and is an array
    const nutritionInfo = Array.isArray(recipe.nutrition_info) ? recipe.nutrition_info : [];
    
    if (nutritionInfo.length === 0) {
      return null;
    }

    return (
      <>
        <Divider sx={{ my: 2 }} />
        <Typography variant="h6" gutterBottom>Nutrition Information</Typography>
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Nutrient</TableCell>
                <TableCell align="right">Amount</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {nutritionInfo.map((nutrient, index) => (
                <TableRow key={index}>
                  <TableCell component="th" scope="row">
                    {nutrient.name}
                  </TableCell>
                  <TableCell align="right">
                    {nutrient.amount} {nutrient.unit}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </>
    );
  };

  return (
    <>
      <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
        <DialogTitle>
          <Box sx={{ mb: 1 }}>
            <Typography variant="h5" component="div">
              {recipe.recipe_name}
            </Typography>
            <Typography variant="subtitle1" color="text.secondary" component="div">
              Cooking Time: {recipe.total_time} minutes
              {averageRating && averageRating.total > 0 && (
                <>
                  {" • "}
                  Average Rating: <StarIcon sx={{ fontSize: 16, mb: -0.3, color: "gold" }} /> {averageRating.average.toFixed(1)} ({averageRating.total} {averageRating.total === 1 ? 'rating' : 'ratings'})
                </>
              )}
            </Typography>
          </Box>
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

          {renderNutritionTable()}
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Close</Button>
          <Button 
            onClick={() => onEat(recipe.recipe_id)}
            startIcon={<RestaurantIcon />}
            variant="contained"
            color="primary"
          >
            {recipe?.is_eaten ? 'I ate this again!' : 'I ate this!'}
          </Button>
          {recipe?.is_eaten && (
            <Button
              onClick={() => {
                console.log('Recipe:', recipe);
                setRatingModalOpen(true);
              }}
              startIcon={<StarIcon />}
              variant="outlined"
              color="primary"
              data-testid="rate-button"
            >
              Rate Recipe
            </Button>
          )}
        </DialogActions>
      </Dialog>

      <RatingModal
        open={ratingModalOpen}
        onClose={() => setRatingModalOpen(false)}
        onSubmit={handleRatingSubmit}
        initialRating={rating}
        isLoading={isLoading}
      />

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