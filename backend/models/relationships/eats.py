from app import db

class Eats(db.Model):
    __tablename__ = 'eats'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), primary_key=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('eats', lazy=True))
    recipe = db.relationship('Recipe', backref=db.backref('eats', lazy=True))

    def __repr__(self):
        return f"<Eats {self.user_id} - {self.recipe_id}>"
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'recipe_id': self.recipe_id,
            'created_at': self.created_at.isoformat()
        }