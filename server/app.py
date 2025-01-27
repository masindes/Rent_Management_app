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
    result = [
        {
            'id': property.id,
            'name': property.name,
            'address': property.address,
            'bedrooms': property.bedrooms,
            'rent': property.rent
        }
        for property in properties
    ]
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


# Update Property
@app.route('/property/<int:id>', methods=['PUT'])
def update_property(id):
    property = Property.query.get_or_404(id)
    data = request.get_json()

    property.name = data['name']
    property.address = data['address']
    property.bedrooms = data['bedrooms']
    property.rent = data['rent']

    db.session.commit()
    return jsonify({'message': 'Property updated successfully'})


# Delete Property
@app.route('/property/<int:id>', methods=['DELETE'])
def delete_property(id):
    property = Property.query.get_or_404(id)
    db.session.delete(property)
    db.session.commit()
    return jsonify({'message': 'Property deleted successfully'})


# Create Tenant
@app.route('/tenant', methods=['POST'])
def create_tenant():
    data = request.get_json()
    new_tenant = Tenant(
        name=data['name'],
        phone=data['phone'],
        unit_id=data['unit_id'],
        email=data['email'],
        property_id=data['property_id']
    )
    db.session.add(new_tenant)
    db.session.commit()
    return jsonify({'message': 'Tenant created successfully'}), 201


# Get All Tenants
@app.route('/tenant', methods=['GET'])
def get_tenants():
    tenants = Tenant.query.all()
    result = [
        {
            'id': tenant.id,
            'name': tenant.name,
            'phone': tenant.phone,
            'unit_id': tenant.unit_id,
            'email': tenant.email,
            'property_id': tenant.property_id
        }
        for tenant in tenants
    ]
    return jsonify(result)


# Get Single Tenant by ID
@app.route('/tenant/<int:id>', methods=['GET'])
def get_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    return jsonify({
        'id': tenant.id,
        'name': tenant.name,
        'phone': tenant.phone,
        'unit_id': tenant.unit_id,
        'email': tenant.email,
        'property_id': tenant.property_id
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


# Create Payment
@app.route('/payment', methods=['POST'])
def create_payment():
    data = request.get_json()
    new_payment = Payment(
        payment_type=data['payment_type'],
        status=data['status'],
        amount=data['amount'],
        payment_date=datetime.strptime(data['payment_date'], '%Y-%m-%d'),
        tenant_id=data['tenant_id']
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Payment created successfully'}), 201


# Get All Payments
@app.route('/payment', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    result = [
        {
            'id': payment.id,
            'payment_type': payment.payment_type,
            'status': payment.status,
            'amount': payment.amount,
            'payment_date': payment.payment_date.strftime('%Y-%m-%d'),
            'tenant_id': payment.tenant_id
        }
        for payment in payments
    ]
    return jsonify(result)


# Get Single Payment by ID
@app.route('/payment/<int:id>', methods=['GET'])
def get_payment(id):
    payment = Payment.query.get_or_404(id)
    return jsonify({
        'id': payment.id,
        'payment_type': payment.payment_type,
        'status': payment.status,
        'amount': payment.amount,
        'payment_date': payment.payment_date.strftime('%Y-%m-%d'),
        'tenant_id': payment.tenant_id
    })


# Update Payment
@app.route('/payment/<int:id>', methods=['PUT'])
def update_payment(id):
    payment = Payment.query.get_or_404(id)
    data = request.get_json()

    payment.payment_type = data['payment_type']
    payment.status = data['status']
    payment.amount = data['amount']
    payment.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d')
    payment.tenant_id = data['tenant_id']

    db.session.commit()
    return jsonify({'message': 'Payment updated successfully'})


# Delete Payment
@app.route('/payment/<int:id>', methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.get_or_404(id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
