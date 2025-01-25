from config.database import db


class UserAgeGroup(db.Model):
    __tablename__ = "user_age_group"

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    age_group = db.Column(db.String(20), nullable=False)

    # Relationship to User model
    user = db.relationship("User", backref="age_group_info")

    def __repr__(self):
        return f"<UserAgeGroup {self.user_id} {self.age_group}>"

    def to_dict(self):
        return {"user_id": self.user_id, "age_group": self.age_group}
