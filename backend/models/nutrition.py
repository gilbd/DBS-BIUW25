from config.database import db


class Nutrition(db.Model):
    __tablename__ = 'nutrition'
    name = db.Column(db.String(45), primary_key=True)
    unit = db.Column(db.String(10), nullable=False)
    average_daily_value = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<Nutrition {self.name}>"
    
    def to_dict(self):
        return {
            'name': self.name,
            'unit': self.unit,
            'average_daily_value': float(self.average_daily_value)
        }
        }
