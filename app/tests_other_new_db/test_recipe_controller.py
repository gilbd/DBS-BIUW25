import unittest
from app import create_app, db
from app.models.recipe import Recipe

class TestRecipeController(unittest.TestCase):
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

    def test_create_recipe(self):
        data = {
            'recipe_name': 'Spaghetti Bolognese',
            'total_time': 30,
            'directions': 'Cook pasta and sauce.',
            'ingredients': 'Pasta, tomatoes, meat, spices'
        }
        response = self.client.post('/recipes', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_recipe(self):
        recipe = Recipe(recipe_name='Spaghetti Bolognese', total_time=30, directions='Cook pasta and sauce.', ingredients='Pasta, tomatoes, meat, spices')
        db.session.add(recipe)
        db.session.commit()

        response = self.client.get(f'/recipes/{recipe.id}')
        self.assertEqual(response.status_code, 200)

    def test_update_recipe(self):
        recipe = Recipe(recipe_name='Spaghetti Bolognese', total_time=30, directions='Cook pasta and sauce.', ingredients='Pasta, tomatoes, meat, spices')
        db.session.add(recipe)
        db.session.commit()

        update_data = {'directions': 'New cooking instructions'}
        response = self.client.put(f'/recipes/{recipe.id}', json=update_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_recipe(self):
        recipe = Recipe(recipe_name='Spaghetti Bolognese', total_time=30, directions='Cook pasta and sauce.', ingredients='Pasta, tomatoes, meat, spices')
        db.session.add(recipe)
        db.session.commit()

        response = self.client.delete(f'/recipes/{recipe.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()