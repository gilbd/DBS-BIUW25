import unittest
from app import create_app, db
from app.models.user import User

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_name="testing")  
        cls.client = cls.app.test_client()  
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_server_is_up(self):
        """בדוק אם השרת רץ ונגיש"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_user_creation(self):
        """בדוק אם אפשר ליצור משתמש דרך ה-API"""
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }
        response = self.client.post('/users', json=data)
        self.assertEqual(response.status_code, 201)

    def test_invalid_route(self):
        response = self.client.get('/invalid_route')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        user = User(name='Jane Doe', email='janedoe@example.com')
        db.session.add(user)
        db.session.commit()
        
        update_data = {'name': 'Janet Doe'}
        response = self.client.put(f'/users/{user.id}', json=update_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        user = User(name='Jane Doe', email='janedoe@example.com')
        db.session.add(user)
        db.session.commit()
        
        response = self.client.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()