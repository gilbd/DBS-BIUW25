from app import db
from app.models.diet import Diet
from app.models.user import User
from app.models.recipe import Recipe
from app.models.admin import Admin
from app.models.nutrition import Nutrition

from app.models.relationships.user_diet import UserDiet
from app.models.relationships.user_nutrition import UserNutrition
from app.models.relationships.eats import Eats
from app.models.relationships.rating import Rating
from app.models.relationships.contains import Contains
from app.models.relationships.fits import Fits