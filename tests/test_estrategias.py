import unittest
from app import db, create_app
from app.models.estrategias import Estrategias

class EstrategiasModelTestCase(unittest.TestCase):
    def setUp(self):
        # Configura la aplicación para pruebas
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Crea una estrategia de prueba
        self.estrategia = Estrategias(
            nombre='Scalping',
            descripcion='Estrategia de trading de alta frecuencia',
            parametros='{}'
        )
        db.session.add(self.estrategia)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_estrategia_creation(self):
        # Verifica que la estrategia se haya creado correctamente
        estrategia = Estrategias.query.filter_by(nombre='Scalping').first()
        self.assertIsNotNone(estrategia)
        self.assertEqual(estrategia.nombre, 'Scalping')
        self.assertEqual(estrategia.descripcion, 'Estrategia de trading de alta frecuencia')
        self.assertEqual(estrategia.parametros, '{}')

    def test_estrategia_update(self):
        # Actualiza y verifica los cambios en la estrategia
        estrategia = Estrategias.query.filter_by(nombre='Scalping').first()
        estrategia.nombre = 'Day Trading'
        estrategia.descripcion = 'Estrategia de trading intradía'
        estrategia.parametros = '{"key": "value"}'
        db.session.commit()

        updated_estrategia = Estrategias.query.filter_by(nombre='Day Trading').first()
        self.assertEqual(updated_estrategia.nombre, 'Day Trading')
        self.assertEqual(updated_estrategia.descripcion, 'Estrategia de trading intradía')
        self.assertEqual(updated_estrategia.parametros, '{"key": "value"}')

    def test_estrategia_delete(self):
        # Elimina la estrategia y verifica que se haya eliminado correctamente
        estrategia = Estrategias.query.filter_by(nombre='Scalping').first()
        db.session.delete(estrategia)
        db.session.commit()

        deleted_estrategia = Estrategias.query.filter_by(nombre='Scalping').first()
        self.assertIsNone(deleted_estrategia)

if __name__ == '__main__':
    unittest.main()
