from app import db

class Contains(db.Model):
    __tablename__ = 'contains'
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True)
    nutrition_name = db.Column(db.String(45), db.ForeignKey('nutrition.name'), primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relationships
    recipe = db.relationship('Recipe', backref=db.backref('contains', lazy=True))
    nutrition = db.relationship('Nutrition', backref=db.backref('contains', lazy=True))

    def __repr__(self):
        return f"<Contains {self.recipe_id} - {self.nutrition_name}>"
    
    def to_dict(self):
        return {
            'recipe_id': self.recipe_id,
            'nutrition_name': self.nutrition_name,
            'amount': float(self.amount)
        }