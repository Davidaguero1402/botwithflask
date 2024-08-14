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

        # Crear un usuario de prueba
        self.user = Usuarios(
            nombre="Carlos",
            apellido="Perez",
            email="carlos.perez@example.com",
            balance=100.0,
            role="User"
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_user_success(self):
        response = self.client.get(f'/users/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['id'], self.user.id)
        self.assertEqual(response_json['nombre'], self.user.nombre)
        self.assertEqual(response_json['apellido'], self.user.apellido)
        self.assertEqual(response_json['email'], self.user.email)
        self.assertEqual(response_json['balance'], self.user.balance)
        self.assertEqual(response_json['role'], self.user.role)

    def test_get_user_not_found(self):
        response = self.client.get('/users/9999')
        self.assertEqual(response.status_code, 404)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['error'], 'User not found')

if __name__ == '__main__':
    unittest.main()

