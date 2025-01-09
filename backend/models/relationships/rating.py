from app import db

class Rating(db.Model):
    __tablename__ = 'rating'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True)
    rating = db.Column(db.SmallInteger, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    user = db.relationship('User', backref=db.backref('rating', lazy=True))
    recipe = db.relationship('Recipe', backref=db.backref('rating', lazy=True))

    def __repr__(self):
        return f"<Rating {self.user_id} - {self.recipe_id}>"
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'recipe_id': self.recipe_id,
            'rating': self.rating,
            'created_at': self.created_at.isoformat()
        }