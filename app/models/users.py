from app import db

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120))
    apellido = db.Column(db.String(120))
    email = db.Column(db.String(120))
    balance = db.Column(db.Float)
    role = db.Column(db.String(50), nullable = False)

    bancos = db.relationship('Bancos', backref='usuario', lazy=True)
    bots = db.relationship('Bots', backref='usuario', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'balance': self.balance,
            'role': self.role
        }
    

    def __init__(self, nombre, apellido, email, balance, role):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.balance = balance
        self.role = role
