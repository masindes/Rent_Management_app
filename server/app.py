from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db, Property, Tenant, Payment
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace(
    'postgres://', 'postgresql://') + '?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Enable CORS
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Error handlers
@app.errorhandler(HTTPException)
def handle_http_error(e):
    return jsonify({
        'error': e.name,
        'message': e.description
    }), e.code

@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    db.session.rollback()
    return jsonify({
        'error': 'Database error',
        'message': str(e)
    }), 500

@app.errorhandler(Exception)
def handle_unexpected_error(e):
    return jsonify({
        'error': 'Unexpected error',
        'message': str(e)
    }), 500

# Helper functions
def validate_json():
    if not request.is_json:
        raise ValueError('Content-Type must be application/json')
    return request.get_json()

def validate_required_fields(data, required_fields):
    missing = [field for field in required_fields if field not in data]
    if missing:
        raise ValueError(f'Missing required fields: {", ".join(missing)}')

# Routes
@app.route("/")
def home():
    return "<h1>Rent Management Application</h1>"

# Property Routes
@app.route('/properties', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    return jsonify([p.to_dict() for p in properties])

@app.route('/properties', methods=['POST'])
def create_property():
    try:
        data = validate_json()
        validate_required_fields(data, ['name', 'address', 'bedrooms', 'rent'])
        
        new_property = Property(**data)
        db.session.add(new_property)
        db.session.commit()
        
        return jsonify({
            'message': 'Property created successfully',
            'property': new_property.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/properties/<int:id>', methods=['GET'])
def get_property(id):
    property = Property.query.get_or_404(id)
    return jsonify(property.to_dict())

@app.route('/properties/<int:id>', methods=['PUT', 'PATCH'])
def update_property(id):
    try:
        property = Property.query.get_or_404(id)
        data = validate_json()
        
        for key, value in data.items():
            if hasattr(property, key):
                setattr(property, key, value)
        
        db.session.commit()
        return jsonify({
            'message': 'Property updated successfully',
            'property': property.to_dict()
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/properties/<int:id>', methods=['DELETE'])
def delete_property(id):
    property = Property.query.get_or_404(id)
    db.session.delete(property)
    db.session.commit()
    return jsonify({'message': 'Property deleted successfully'})

# Tenant Routes
@app.route('/tenants', methods=['GET'])
def get_tenants():
    tenants = Tenant.query.all()
    return jsonify([t.to_dict() for t in tenants])

@app.route('/tenants', methods=['POST'])
def create_tenant():
    try:
        data = validate_json()
        validate_required_fields(data, ['name', 'phone', 'email', 'unit_id', 'property_id'])
        
        new_tenant = Tenant(**data)
        db.session.add(new_tenant)
        db.session.commit()
        
        return jsonify({
            'message': 'Tenant created successfully',
            'tenant': new_tenant.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/tenants/<int:id>', methods=['GET'])
def get_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    return jsonify(tenant.to_dict())

@app.route('/tenants/<int:id>', methods=['PATCH'])
def update_tenant(id):
    try:
        tenant = Tenant.query.get_or_404(id)
        data = validate_json()
        
        for key, value in data.items():
            if hasattr(tenant, key):
                setattr(tenant, key, value)
        
        db.session.commit()
        return jsonify({
            'message': 'Tenant updated successfully',
            'tenant': tenant.to_dict()
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/tenants/<int:id>', methods=['DELETE'])
def delete_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    db.session.delete(tenant)
    db.session.commit()
    return jsonify({'message': 'Tenant deleted successfully'})

# Payment Routes
@app.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([p.to_dict() for p in payments])

@app.route('/payments', methods=['POST'])
def create_payment():
    try:
        data = validate_json()
        validate_required_fields(data, ['payment_type', 'status', 'amount', 'payment_date', 'tenant_id'])
        
        try:
            data['payment_date'] = datetime.strptime(data['payment_date'], '%Y-%m-%d')
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')
        
        new_payment = Payment(**data)
        db.session.add(new_payment)
        db.session.commit()
        
        return jsonify({
            'message': 'Payment created successfully',
            'payment': new_payment.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/payments/<int:id>', methods=['GET'])
def get_payment(id):
    payment = Payment.query.get_or_404(id)
    return jsonify(payment.to_dict())

@app.route('/payments/<int:id>', methods=['PATCH'])
def update_payment(id):
    try:
        payment = Payment.query.get_or_404(id)
        data = validate_json()
        
        if 'payment_date' in data:
            try:
                data['payment_date'] = datetime.strptime(data['payment_date'], '%Y-%m-%d')
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        
        for key, value in data.items():
            if hasattr(payment, key):
                setattr(payment, key, value)
        
        db.session.commit()
        return jsonify({
            'message': 'Payment updated successfully',
            'payment': payment.to_dict()
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.get_or_404(id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted successfully'})

# Database teardown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', False))