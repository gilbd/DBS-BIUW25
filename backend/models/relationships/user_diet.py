from app import db

class UserDiet(db.Model):
    __tablename__ = 'user_diet'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diet.diet_id'), primary_key=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('user_diet', lazy=True))
    diet = db.relationship('Diet', backref=db.backref('user_diet', lazy=True))

    def __repr__(self):
        return f"<UserDiet {self.user_id} - {self.diet_id}>"
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'diet_id': self.diet_id
        }