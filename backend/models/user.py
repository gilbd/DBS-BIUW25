from config.database import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "date_of_birth": self.date_of_birth.isoformat(),
            "weight": self.weight,
            "height": self.height,
            "sex": self.sex,
            "email": self.email,
        }
