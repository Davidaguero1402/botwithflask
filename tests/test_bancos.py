import unittest
from app import db, create_app
from app.models.users import Usuarios
from app.models.bancos import Bancos

class BancosModelTestCase(unittest.TestCase):
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

        # Crea un banco de prueba
        self.banco = Bancos(
            nombre='Banco Nación',
            cuenta='123456789',
            usuario_id=self.usuario.id
        )
        db.session.add(self.banco)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_banco_creation(self):
        # Verifica que el banco se haya creado correctamente
        banco = Bancos.query.filter_by(nombre='Banco Nación').first()
        self.assertIsNotNone(banco)
        self.assertEqual(banco.nombre, 'Banco Nación')
        self.assertEqual(banco.cuenta, '123456789')
        self.assertEqual(banco.usuario_id, self.usuario.id)

    def test_banco_update(self):
        # Actualiza y verifica los cambios en el banco
        banco = Bancos.query.filter_by(nombre='Banco Nación').first()
        banco.nombre = 'Banco Provincia'
        banco.cuenta = '987654321'
        db.session.commit()

        updated_banco = Bancos.query.filter_by(nombre='Banco Provincia').first()
        self.assertEqual(updated_banco.nombre, 'Banco Provincia')
        self.assertEqual(updated_banco.cuenta, '987654321')

    def test_banco_delete(self):
        # Elimina el banco y verifica que se haya eliminado correctamente
        banco = Bancos.query.filter_by(nombre='Banco Nación').first()
        db.session.delete(banco)
        db.session.commit()

        deleted_banco = Bancos.query.filter_by(nombre='Banco Nación').first()
        self.assertIsNone(deleted_banco)

if __name__ == '__main__':
    unittest.main()