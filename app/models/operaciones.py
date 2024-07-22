from app import db

class Operaciones(db.Model):
    __tablename__ = 'Operaciones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('Bots.id'), nullable=False)
    activo_id = db.Column(db.Integer, db.ForeignKey('Activos.id'), nullable=False)
    tipo_operacion = db.Column(db.String(50))
    precio = db.Column(db.Float)
    cantidad = db.Column(db.Float)
    fecha = db.Column(db.DateTime)