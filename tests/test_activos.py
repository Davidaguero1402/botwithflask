import unittest
from app import db, create_app
from app.models.activos import Activos

class ActivosModelTestCase(unittest.TestCase):
    def setUp(self):
        # Configura la aplicación para pruebas
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Crea un activo de prueba
        self.activo = Activos(
            nombre='Bitcoin',
            simbolo='BTC',
            tipo='Criptomoneda'
        )
        db.session.add(self.activo)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_activo_creation(self):
        # Verifica que el activo se haya creado correctamente
        activo = Activos.query.filter_by(nombre='Bitcoin').first()
        self.assertIsNotNone(activo)
        self.assertEqual(activo.nombre, 'Bitcoin')
        self.assertEqual(activo.simbolo, 'BTC')
        self.assertEqual(activo.tipo, 'Criptomoneda')

    def test_activo_update(self):
        # Actualiza y verifica los cambios en el activo
        activo = Activos.query.filter_by(nombre='Bitcoin').first()
        activo.nombre = 'Ethereum'
        activo.simbolo = 'ETH'
        activo.tipo = 'Criptomoneda'
        db.session.commit()

        updated_activo = Activos.query.filter_by(nombre='Ethereum').first()
        self.assertEqual(updated_activo.nombre, 'Ethereum')
        self.assertEqual(updated_activo.simbolo, 'ETH')

    def test_activo_delete(self):
        # Elimina el activo y verifica que se haya eliminado correctamente
        activo = Activos.query.filter_by(nombre='Bitcoin').first()
        db.session.delete(activo)
        db.session.commit()

        deleted_activo = Activos.query.filter_by(nombre='Bitcoin').first()
        self.assertIsNone(deleted_activo)

if __name__ == '__main__':
    unittest.main()
