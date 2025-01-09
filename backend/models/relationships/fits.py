from app import db

class Fits(db.Model):
    __tablename__ = 'fits'
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diet.diet_id'), primary_key=True)
    
    # Relationships
    recipe = db.relationship('Recipe', backref=db.backref('fits', lazy=True))
    diet = db.relationship('Diet', backref=db.backref('fits', lazy=True))

    def __repr__(self):
        return f"<Fits {self.recipe_id} - {self.diet_id}>"
    
    def to_dict(self):
        return {
            'recipe_id': self.recipe_id,
            'diet_id': self.diet_id
        }