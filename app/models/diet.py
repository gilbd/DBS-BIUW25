from app import db

class Diet(db.Model):
    __tablename__ = 'diet'
    diet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    keywords = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Diet {self.name}>"
    
    def to_dict(self):
        return {
            'diet_id': self.diet_id,
            'name': self.name,
            'keywords': self.keywords,
            'description': self.description
        }