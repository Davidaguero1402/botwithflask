from app import db

class Bancos(db.Model):
    __tablename__ = 'Bancos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120))
    cuenta = db.Column(db.String(120))
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)