import unittest

from config.database import create_app, db
from models.nutrition import Nutrition
from models.relationships.user_nutrition import UserNutrition
from models.user import User


class TestUserNutritionController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_track_user_nutrition(self):
        user = User(name='John Doe', email='johndoe@example.com')
        nutrition = Nutrition(name='Vitamin C', description='Immune boosting')
        db.session.add(user)
        db.session.add(nutrition)
        db.session.commit()

        data = {
            'user_id': user.id,
            'nutrition_name': nutrition.name,
            'tracked_value': 100
        }
        response = self.client.post('/user_nutrition', json=data)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()if __name__ == '__main__':
    unittest.main()