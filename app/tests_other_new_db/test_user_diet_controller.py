import unittest
from app import create_app, db
from app.models.relationships.user_diet import UserDiet
from app.models.user import User
from app.models.diet import Diet

class TestUserDietController(unittest.TestCase):
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

    def test_add_user_diet(self):
        user = User(name='John Doe', email='johndoe@example.com')
        diet = Diet(name='Keto', description='Low-carb diet')
        db.session.add(user)
        db.session.add(diet)
        db.session.commit()

        data = {
            'user_id': user.id,
            'diet_id': diet.id
        }
        response = self.client.post('/user_diets', json=data)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()