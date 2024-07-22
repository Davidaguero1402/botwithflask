from app import db

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120))
    apellido = db.Column(db.String(120))
    email = db.Column(db.String(120))
    balance = db.Column(db.Float)
    autenticacion = db.Column(db.String(255))

    bancos = db.relationship('Bancos', backref='usuario', lazy=True)
    bots = db.relationship('Bots', backref='usuario', lazy=True)
