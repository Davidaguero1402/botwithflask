import unittest
from datetime import datetime
from app import db, create_app
from app.models.bots import Bots
from app.models.activos import Activos
from app.models.operaciones import Operaciones
from app.models.users import Usuarios
from app.models.exchanges import Exchanges
from app.models.estrategias import Estrategias

class OperacionesModelTestCase(unittest.TestCase):
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

        # Crea una operación de prueba
        self.operacion = Operaciones(
            bot_id=self.bot.id,
            activo_id=self.activo.id,
            tipo_operacion='Compra',
            precio=50000.0,
            cantidad=0.1,
            fecha=datetime.utcnow()
        )
        db.session.add(self.operacion)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_operacion_creation(self):
        # Verifica que la operación se haya creado correctamente
        operacion = Operaciones.query.filter_by(bot_id=self.bot.id).first()
        self.assertIsNotNone(operacion)
        self.assertEqual(operacion.bot_id, self.bot.id)
        self.assertEqual(operacion.activo_id, self.activo.id)
        self.assertEqual(operacion.tipo_operacion, 'Compra')
        self.assertEqual(operacion.precio, 50000.0)
        self.assertEqual(operacion.cantidad, 0.1)

    def test_operacion_update(self):
        # Actualiza y verifica los cambios en la operación
        operacion = Operaciones.query.filter_by(bot_id=self.bot.id).first()
        operacion.tipo_operacion = 'Venta'
        operacion.precio = 55000.0
        operacion.cantidad = 0.05
        db.session.commit()

        updated_operacion = Operaciones.query.filter_by(bot_id=self.bot.id).first()
        self.assertEqual(updated_operacion.tipo_operacion, 'Venta')
        self.assertEqual(updated_operacion.precio, 55000.0)
        self.assertEqual(updated_operacion.cantidad, 0.05)

    def test_operacion_delete(self):
        # Elimina la operación y verifica que se haya eliminado correctamente
        operacion = Operaciones.query.filter_by(bot_id=self.bot.id).first()
        db.session.delete(operacion)
        db.session.commit()

        deleted_operacion = Operaciones.query.filter_by(bot_id=self.bot.id).first()
        self.assertIsNone(deleted_operacion)

if __name__ == '__main__':
    unittest.main()
