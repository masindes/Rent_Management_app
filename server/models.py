from app import db


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    rent = db.Column(db.Float, nullable=False)
    tenants = db.relationship('Tenant', backref='property', lazy=True)

    def __repr__(self):
        return f'<Property {self.name} , Address{self.address}, Bedrooms{self.bedrooms}, Rent{self.rent}>' 
    

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    unit_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    payments = db.relationship('Payment', backref='tenant', lazy=True)

    def __repr__(self):
        return f'<Tenant {self.name} , Phone:{self.phone}, Unit_id:{self.unit_id}, Email:{self.email}>'
