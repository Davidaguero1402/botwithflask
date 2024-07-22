from app import db

class Bots(db.Model):
    __tablename__ = 'Bots'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    exchange_id = db.Column(db.Integer, db.ForeignKey('Exchanges.id'), nullable=False)
    activo_id = db.Column(db.Integer, db.ForeignKey('Activos.id'), nullable=False)
    estrategia_id = db.Column(db.Integer, db.ForeignKey('Estrategias.id'), nullable=False)

    operaciones = db.relationship('Operaciones', backref='bot', lazy=True)
