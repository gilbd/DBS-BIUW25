from app import db

class Admin(db.Model):
    __tablename__ = 'admin'
    
    admin_id = db.Column(db.Integer, primary_key=True)  # Primary Key
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Foreign Key referencing 'user'
    promoted_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp of promotion
    
    # Relationship to User model
    user = db.relationship('User', backref=db.backref('admin', uselist=False), lazy=True)

    def __repr__(self):
        return f"<Admin {self.user_id}>"
    
    def to_dict(self):
        """Converts the Admin model to a dictionary representation."""
        return {
            'admin_id': self.admin_id,
            'user_id': self.user_id,
            'promoted_at': self.promoted_at
        }