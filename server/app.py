from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db, Property, Tenant, Payment
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://rent_management_app_user:7BjZevxGsQkFasEeL5TW2vyiEpnlDJiB@dpg-cuf0oa56l47c73f8l3j0-a.oregon-postgres.render.com/rent_management_app"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:3000",
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})


@app.route("/")
def home():
    return "<h1>Rent Management Application</h1>"

# Helper function to handle not found errors
def handle_not_found(item, id):
    if not item:
        return jsonify({'error': f'Item with ID {id} not found'}), 404
    return None

# Routes for Properties
@app.route('/property', methods=['POST'])
def create_property():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    required_fields = ['name', 'address', 'bedrooms', 'rent']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_property = Property(**data)
    db.session.add(new_property)
    db.session.commit()
    return jsonify({'message': 'Property created successfully', 'property': new_property.to_dict()}), 201

@app.route('/property', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    return jsonify([p.to_dict() for p in properties])

@app.route('/property/<int:id>', methods=['GET'])
def get_property(id):
    property = Property.query.get(id)
    error = handle_not_found(property, id)
    if error:
        return error
    return jsonify(property.to_dict())

@app.route('/property/<int:id>', methods=['PUT', 'PATCH'])  # Allow both PUT and PATCH
def update_property(id):
    property = Property.query.get(id)
    error = handle_not_found(property, id)
    if error:
        return error

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    for key, value in data.items():
        if hasattr(property, key):
            setattr(property, key, value)
    db.session.commit()
    return jsonify({'message': 'Property updated successfully', 'property': property.to_dict()})

@app.route('/property/<int:id>', methods=['DELETE'])
def delete_property(id):
    property = Property.query.get(id)
    error = handle_not_found(property, id)
    if error:
        return error

    db.session.delete(property)
    db.session.commit()
    return jsonify({'message': 'Property deleted successfully'})

# Routes for Tenants
@app.route('/tenant', methods=['POST'])
def create_tenant():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    required_fields = ['name', 'phone', 'email', 'unit_id', 'property_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_tenant = Tenant(**data)
    db.session.add(new_tenant)
    db.session.commit()
    return jsonify({'message': 'Tenant created successfully', 'tenant': new_tenant.to_dict()}), 201

@app.route('/tenant', methods=['GET'])
def get_tenants():
    tenants = Tenant.query.all()
    return jsonify([t.to_dict() for t in tenants])

@app.route('/tenant/<int:id>', methods=['GET'])
def get_tenant(id):
    tenant = Tenant.query.get(id)
    error = handle_not_found(tenant, id)
    if error:
        return error
    return jsonify(tenant.to_dict())

@app.route('/tenant/<int:id>', methods=['PATCH'])
def patch_tenant(id):
    tenant = Tenant.query.get(id)
    error = handle_not_found(tenant, id)
    if error:
        return error

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    for key, value in data.items():
        if hasattr(tenant, key):
            setattr(tenant, key, value)
    db.session.commit()
    return jsonify({'message': 'Tenant updated successfully', 'tenant': tenant.to_dict()})

@app.route('/tenant/<int:id>', methods=['DELETE'])
def delete_tenant(id):
    tenant = Tenant.query.get(id)
    error = handle_not_found(tenant, id)
    if error:
        return error

    db.session.delete(tenant)
    db.session.commit()
    return jsonify({'message': 'Tenant deleted successfully'})

# Routes for Payments
@app.route('/payment', methods=['POST'])
def create_payment():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    required_fields = ['payment_type', 'status', 'amount', 'payment_date', 'tenant_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        data['payment_date'] = datetime.strptime(data['payment_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    new_payment = Payment(**data)
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Payment created successfully', 'payment': new_payment.to_dict()}), 201

@app.route('/payment', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([p.to_dict() for p in payments])

@app.route('/payment/<int:id>', methods=['GET'])
def get_payment(id):
    payment = Payment.query.get(id)
    error = handle_not_found(payment, id)
    if error:
        return error
    return jsonify(payment.to_dict())

@app.route('/payment/<int:id>', methods=['PATCH'])
def patch_payment(id):
    payment = Payment.query.get(id)
    error = handle_not_found(payment, id)
    if error:
        return error

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    if 'payment_date' in data:
        try:
            data['payment_date'] = datetime.strptime(data['payment_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    for key, value in data.items():
        if hasattr(payment, key):
            setattr(payment, key, value)
    db.session.commit()
    return jsonify({'message': 'Payment updated successfully', 'payment': payment.to_dict()})

@app.route('/payment/<int:id>', methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.get(id)
    error = handle_not_found(payment, id)
    if error:
        return error

    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)