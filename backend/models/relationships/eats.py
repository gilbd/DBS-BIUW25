from datetime import datetime

from config.database import db


class Eats(db.Model):
    __tablename__ = "eats"

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)

    # Relationships
    user = db.relationship("User", backref="eats")
    recipe = db.relationship("Recipe", backref="eats")

    def __repr__(self):
        return f"<Eats user_id={self.user_id} recipe_id={self.recipe_id}>"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "recipe_id": self.recipe_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
