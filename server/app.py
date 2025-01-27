from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import Property, Tenant, Payment


# Initialize the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rent_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app)

# Create Property
@app.route('/property', methods=['POST'])
def create_property():
    data = request.get_json()
    new_property = Property(
        name=data['name'],
        address=data['address'],
        bedrooms=data['bedrooms'],
        rent=data['rent']
    )
    db.session.add(new_property)
    db.session.commit()
    return jsonify({'message': 'Property created successfully'}), 201

# Get All Properties
@app.route('/property', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    result = []
    for property in properties:
        result.append({
            'id': property.id,
            'name': property.name,
            'address': property.address,
            'bedrooms': property.bedrooms,
            'rent': property.rent
        })
    return jsonify(result)

# Get Single Property by ID
@app.route('/property/<int:id>', methods=['GET'])
def get_property(id):
    property = Property.query.get_or_404(id)
    return jsonify({
        'id': property.id,
        'name': property.name,
        'address': property.address,
        'bedrooms': property.bedrooms,
        'rent': property.rent
    })

# Update Tenant
@app.route('/tenant/<int:id>', methods=['PUT'])
def update_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    data = request.get_json()

    tenant.name = data['name']
    tenant.phone = data['phone']
    tenant.unit_id = data['unit_id']
    tenant.email = data['email']
    tenant.property_id = data['property_id']

    db.session.commit()
    return jsonify({'message': 'Tenant updated successfully'})

# Delete Tenant
@app.route('/tenant/<int:id>', methods=['DELETE'])
def delete_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    db.session.delete(tenant)
    db.session.commit()
    return jsonify({'message': 'Tenant deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
