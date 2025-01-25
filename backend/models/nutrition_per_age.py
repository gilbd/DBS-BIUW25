from config.database import db


class NutritionPerAge(db.Model):
    __tablename__ = "nutrition_per_age"

    age_group = db.Column(db.String(20), primary_key=True)
    sex = db.Column(db.Enum("M", "F"), primary_key=True)
    nutrition_name = db.Column(db.String(45), db.ForeignKey("nutrition.name"), primary_key=True)
    recommended_daily_value = db.Column(db.Decimal(10, 2), nullable=False)

    # Relationship to Nutrition model
    nutrition = db.relationship("Nutrition", backref="age_recommendations")

    def __repr__(self):
        return f"<NutritionPerAge {self.age_group} {self.sex} {self.nutrition_name}>"

    def to_dict(self):
        return {
            "age_group": self.age_group,
            "sex": self.sex,
            "nutrition_name": self.nutrition_name,
            "recommended_daily_value": float(self.recommended_daily_value),
        }
