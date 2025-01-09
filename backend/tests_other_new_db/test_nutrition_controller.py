import unittest
from app import create_app, db
from app.models.nutrition import Nutrition

class TestNutritionController(unittest.TestCase):
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

    def test_create_nutrition(self):
        data = {
            'name': 'Vitamin C',
            'description': 'An essential vitamin for immune function'
        }
        response = self.client.post('/nutrition', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_nutrition(self):
        nutrition = Nutrition(name='Vitamin C', description='Essential for immune function')
        db.session.add(nutrition)
        db.session.commit()

        response = self.client.get(f'/nutrition/{nutrition.name}')
        self.assertEqual(response.status_code, 200)

    def test_update_nutrition(self):
        nutrition = Nutrition(name='Vitamin C', description='Essential for immune function')
        db.session.add(nutrition)
        db.session.commit()

        update_data = {'description': 'Updated description for Vitamin C'}
        response = self.client.put(f'/nutrition/{nutrition.name}', json=update_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_nutrition(self):
        nutrition = Nutrition(name='Vitamin C', description='Essential for immune function')
        db.session.add(nutrition)
        db.session.commit()

        response = self.client.delete(f'/nutrition/{nutrition.name}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()