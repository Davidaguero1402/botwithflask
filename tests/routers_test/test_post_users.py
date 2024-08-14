# tests/test_post_users.py
import unittest
import json
from app import create_app, db
from app.models.users import Usuarios

class UserRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user_success(self):
        user_data = {
            "nombre": "Ana",
            "apellido": "Gomez",
            "email": "ana.gomez@example.com",
            "balance": 150.0,
            "role": "User"
        }

        response = self.client.post('/users/', data=json.dumps(user_data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['message'], 'Usuario creado con éxito')
        self.assertEqual(response_json['user']['nombre'], 'Ana')
        self.assertEqual(response_json['user']['apellido'], 'Gomez')
        self.assertEqual(response_json['user']['email'], 'ana.gomez@example.com')
        self.assertEqual(response_json['user']['balance'], 150.0)
        self.assertEqual(response_json['user']['role'], 'User')

    def test_create_user_missing_data(self):
        user_data = {
            "nombre": "Ana",
        }

        response = self.client.post('/users/', data=json.dumps(user_data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['message'], 'Datos incompletos')

    def test_create_user_duplicate(self):
        user_data = {
            "nombre": "Luis",
            "apellido": "Martinez",
            "email": "luis.martinez@example.com",
            "balance": 200.0,
            "role": "User"
        }
        self.client.post('/users/', data=json.dumps(user_data), content_type='application/json')

        response = self.client.post('/users/', data=json.dumps(user_data), content_type='application/json')

        self.assertEqual(response.status_code, 409)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['message'], 'El usuario ya existe')

if __name__ == '__main__':
    unittest.main()
