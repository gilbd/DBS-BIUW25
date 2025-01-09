from app import db

class Recipe(db.Model):
    __tablename__ = 'recipe'
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(255), nullable=False)
    total_time = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    directions = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Recipe {self.recipe_name}>"
    
    def to_dict(self):
        return {
            'recipe_id': self.recipe_id,
            'recipe_name': self.recipe_name,
            'total_time': self.total_time,
            'image': self.image,
            'directions': self.directions,
            'ingredients': self.ingredients
        }