import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Rating,
  Box,
  Typography,
  CircularProgress
} from '@mui/material';
import StarIcon from '@mui/icons-material/Star';

function RatingModal({ open, onClose, onSubmit, initialRating = 0, isLoading }) {
  const [hover, setHover] = React.useState(-1);
  const [value, setValue] = React.useState(initialRating);

  const labels = {
    1: 'Poor',
    2: 'Fair',
    3: 'Good',
    4: 'Very Good',
    5: 'Excellent'
  };

  const handleSubmit = () => {
    if (value > 0) {
      onSubmit(value);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ textAlign: 'center' }}>Rate this Recipe</DialogTitle>
      <DialogContent>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 2,
            py: 3
          }}
        >
          <Rating
            size="large"
            value={value}
            onChange={(event, newValue) => {
              setValue(newValue);
            }}
            onChangeActive={(event, newHover) => {
              setHover(newHover);
            }}
            emptyIcon={<StarIcon style={{ opacity: 0.55 }} fontSize="inherit" />}
            disabled={isLoading}
          />
          {value !== null && (
            <Typography variant="h6" sx={{ mt: 1 }}>
              {labels[hover !== -1 ? hover : value]}
            </Typography>
          )}
          {isLoading && <CircularProgress size={24} />}
        </Box>
      </DialogContent>
      <DialogActions sx={{ justifyContent: 'center', pb: 2 }}>
        <Button onClick={onClose} variant="outlined" disabled={isLoading}>
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={value === 0 || isLoading}
        >
          Submit Rating
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default RatingModal; 