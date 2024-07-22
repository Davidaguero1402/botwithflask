import unittest
from app import db, create_app
from app.models.users import Usuarios
from app.models.exchanges import Exchanges
from app.models.activos import Activos
from app.models.estrategias import Estrategias
from app.models.bots import Bots

class BotsModelTestCase(unittest.TestCase):
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

        # Crea un exchange de prueba
        self.exchange = Exchanges(
            nombre='Binance',
            api_key='apikey123',
            secret_key='secretkey123'
        )
        db.session.add(self.exchange)
        db.session.commit()

        # Crea un activo de prueba
        self.activo = Activos(
            nombre='Bitcoin',
            simbolo='BTC',
            tipo='Criptomoneda'
        )
        db.session.add(self.activo)
        db.session.commit()

        # Crea una estrategia de prueba
        self.estrategia = Estrategias(
            nombre='Scalping',
            descripcion='Estrategia de trading de alta frecuencia'
        )
        db.session.add(self.estrategia)
        db.session.commit()

        # Crea un bot de prueba
        self.bot = Bots(
            usuario_id=self.usuario.id,
            exchange_id=self.exchange.id,
            activo_id=self.activo.id,
            estrategia_id=self.estrategia.id
        )
        db.session.add(self.bot)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_bot_creation(self):
        # Verifica que el bot se haya creado correctamente
        bot = Bots.query.filter_by(usuario_id=self.usuario.id).first()
        self.assertIsNotNone(bot)
        self.assertEqual(bot.usuario_id, self.usuario.id)
        self.assertEqual(bot.exchange_id, self.exchange.id)
        self.assertEqual(bot.activo_id, self.activo.id)
        self.assertEqual(bot.estrategia_id, self.estrategia.id)

    def test_bot_update(self):
        # Actualiza y verifica los cambios en el bot
        bot = Bots.query.filter_by(usuario_id=self.usuario.id).first()
        nuevo_activo = Activos(
            nombre='Ethereum',
            simbolo='ETH',
            tipo='Criptomoneda'
        )
        db.session.add(nuevo_activo)
        db.session.commit()

        bot.activo_id = nuevo_activo.id
        db.session.commit()

        updated_bot = Bots.query.filter_by(usuario_id=self.usuario.id).first()
        self.assertEqual(updated_bot.activo_id, nuevo_activo.id)

    def test_bot_delete(self):
        # Elimina el bot y verifica que se haya eliminado correctamente
        bot = Bots.query.filter_by(usuario_id=self.usuario.id).first()
        db.session.delete(bot)
        db.session.commit()

        deleted_bot = Bots.query.filter_by(usuario_id=self.usuario.id).first()
        self.assertIsNone(deleted_bot)

if __name__ == '__main__':
    unittest.main()
