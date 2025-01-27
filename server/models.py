from app import db


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    rent = db.Column(db.Float, nullable=False)
    tenants = db.relationship('Tenant', backref='property', lazy=True)
