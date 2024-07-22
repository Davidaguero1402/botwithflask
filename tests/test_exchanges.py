import unittest
from app import db, create_app
from app.models.exchanges import Exchanges

class ExchangesModelTestCase(unittest.TestCase):
    def setUp(self):
        # Configura la aplicación para pruebas
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Crea un exchange de prueba
        self.exchange = Exchanges(
            nombre='Binance',
            api_key='apikey123',
            secret_key='secretkey123'
        )
        db.session.add(self.exchange)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_exchange_creation(self):
        # Verifica que el exchange se haya creado correctamente
        exchange = Exchanges.query.filter_by(nombre='Binance').first()
        self.assertIsNotNone(exchange)
        self.assertEqual(exchange.nombre, 'Binance')
        self.assertEqual(exchange.api_key, 'apikey123')
        self.assertEqual(exchange.secret_key, 'secretkey123')

    def test_exchange_update(self):
        # Actualiza y verifica los cambios en el exchange
        exchange = Exchanges.query.filter_by(nombre='Binance').first()
        exchange.nombre = 'Coinbase'
        exchange.api_key = 'newapikey123'
        exchange.secret_key = 'newsecretkey123'
        db.session.commit()

        updated_exchange = Exchanges.query.filter_by(nombre='Coinbase').first()
        self.assertEqual(updated_exchange.nombre, 'Coinbase')
        self.assertEqual(updated_exchange.api_key, 'newapikey123')
        self.assertEqual(updated_exchange.secret_key, 'newsecretkey123')

    def test_exchange_delete(self):
        # Elimina el exchange y verifica que se haya eliminado correctamente
        exchange = Exchanges.query.filter_by(nombre='Binance').first()
        db.session.delete(exchange)
        db.session.commit()

        deleted_exchange = Exchanges.query.filter_by(nombre='Binance').first()
        self.assertIsNone(deleted_exchange)

if __name__ == '__main__':
    unittest.main()
