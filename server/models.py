from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    rent = db.Column(db.Float, nullable=False)
    tenants = db.relationship('Tenant', backref='property', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'bedrooms': self.bedrooms,
            'rent': self.rent
        }

class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    unit_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    payments = db.relationship('Payment', backref='tenant', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'unit_id': self.unit_id,
            'email': self.email,
            'property_id': self.property_id
        }

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    payment_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'payment_type': self.payment_type,
            'status': self.status,
            'amount': self.amount,
            'payment_date': self.payment_date.strftime('%Y-%m-%d'),
            'tenant_id': self.tenant_id
        }
