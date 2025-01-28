from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db, Property, Tenant, Payment

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rent_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

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

    new_property = Property(**data)
    db.session.add(new_property)
    db.session.commit()
    return jsonify({'message': 'Property created successfully'}), 201

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


@app.route('/property/<int:id>', methods=['PATCH'])
def patch_property(id):
    property = Property.query.get(id)
    error = handle_not_found(property, id)
    if error:
        return error

    data = request.get_json()
    for key, value in data.items():
        setattr(property, key, value)
    db.session.commit()
    return jsonify({'message': 'Property updated successfully'})


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

    new_tenant = Tenant(**data)
    db.session.add(new_tenant)
    db.session.commit()
    return jsonify({'message': 'Tenant created successfully'}), 201

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
    for key, value in data.items():
        setattr(tenant, key, value)
    db.session.commit()
    return jsonify({'message': 'Tenant updated successfully'})

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

    data['payment_date'] = datetime.strptime(data['payment_date'], '%Y-%m-%d')
    new_payment = Payment(**data)
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Payment created successfully'}), 201

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
    if 'payment_date' in data:
        data['payment_date'] = datetime.strptime(data['payment_date'], '%Y-%m-%d')
    for key, value in data.items():
        setattr(payment, key, value)
    db.session.commit()
    return jsonify({'message': 'Payment updated successfully'})

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
