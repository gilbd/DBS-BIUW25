from app import db

class UserNutrition(db.Model):
    __tablename__ = 'user_nutrition'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    nutrition_name = db.Column(db.String(45), db.ForeignKey('nutrition.name'), primary_key=True)
    tracked_value = db.Column(db.Numeric(10, 2), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('user_nutrition', lazy=True))
    nutrition = db.relationship('Nutrition', backref=db.backref('user_nutrition', lazy=True))

    def __repr__(self):
        return f"<UserNutrition {self.user_id} - {self.nutrition_name}>"
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'nutrition_name': self.nutrition_name,
            'tracked_value': float(self.tracked_value) if self.tracked_value is not None else None
        }