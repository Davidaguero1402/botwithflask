import unittest
from app import db, create_app
from app.models.users import Usuarios
from app.models.bancos import Bancos

class UsuariosModelTestCase(unittest.TestCase):
    def setUp(self):
        # Configura la aplicación para pruebas
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Crea un usuario de prueba
        self.usuario = Usuarios(
            nombre='Juan',
            apellido='Perez',
            email='juan.perez@example.com',
            balance=100.0,
            autenticacion='token123'
        )
        db.session.add(self.usuario)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_usuario_creation(self):
        # Verifica que el usuario se haya creado correctamente
        usuario = Usuarios.query.filter_by(email='juan.perez@example.com').first()
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, 'Juan')
        self.assertEqual(usuario.apellido, 'Perez')
        self.assertEqual(usuario.email, 'juan.perez@example.com')
        self.assertEqual(usuario.balance, 100.0)
        self.assertEqual(usuario.autenticacion, 'token123')

    def test_usuario_update(self):
        # Actualiza y verifica los cambios en el usuario
        usuario = Usuarios.query.filter_by(email='juan.perez@example.com').first()
        usuario.nombre = 'Carlos'
        usuario.balance = 200.0
        db.session.commit()

        updated_usuario = Usuarios.query.filter_by(email='juan.perez@example.com').first()
        self.assertEqual(updated_usuario.nombre, 'Carlos')
        self.assertEqual(updated_usuario.balance, 200.0)

    def test_usuario_delete(self):
        # Elimina el usuario y verifica que se haya eliminado correctamente
        usuario = Usuarios.query.filter_by(email='juan.perez@example.com').first()
        db.session.delete(usuario)
        db.session.commit()

        deleted_usuario = Usuarios.query.filter_by(email='juan.perez@example.com').first()
        self.assertIsNone(deleted_usuario)

if __name__ == '__main__':
    unittest.main()
