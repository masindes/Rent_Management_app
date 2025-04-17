from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db, Property, Tenant, Payment
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace(
    'postgres://', 'postgresql://') + '?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Enable CORS
CORS(app)

# Error handlers
@app.errorhandler(HTTPException)
def handle_http_error(e):
    return jsonify({
        'success': False,
        'error': e.name,
        'message': e.description
    }), e.code

@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 'Database error',
        'message': str(e)
    }), 500

@app.errorhandler(Exception)
def handle_unexpected_error(e):
    return jsonify({
        'success': False,
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

def get_pagination_params():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return page, per_page

# Property CRUD Operations
@app.route('/api/properties', methods=['GET', 'POST'])
def handle_properties():
    if request.method == 'GET':
        page, per_page = get_pagination_params()
        properties = Property.query.paginate(page=page, per_page=per_page)
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in properties.items],
            'total': properties.total,
            'pages': properties.pages,
            'current_page': properties.page
        })
    
    elif request.method == 'POST':
        try:
            data = validate_json()
            validate_required_fields(data, ['name', 'address', 'bedrooms', 'rent'])
            
            new_property = Property(
                name=data['name'],
                address=data['address'],
                bedrooms=data['bedrooms'],
                rent=data['rent']
            )
            db.session.add(new_property)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': new_property.to_dict()
            }), 201
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400

@app.route('/api/properties/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_property(id):
    property = Property.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'data': property.to_dict()
        })
    
    elif request.method == 'PUT':
        try:
            data = validate_json()
            
            property.name = data.get('name', property.name)
            property.address = data.get('address', property.address)
            property.bedrooms = data.get('bedrooms', property.bedrooms)
            property.rent = data.get('rent', property.rent)
            
            db.session.commit()
            return jsonify({
                'success': True,
                'data': property.to_dict()
            })
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400
    
    elif request.method == 'DELETE':
        db.session.delete(property)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Property deleted successfully'
        })

# Tenant CRUD Operations
@app.route('/api/tenants', methods=['GET', 'POST'])
def handle_tenants():
    if request.method == 'GET':
        page, per_page = get_pagination_params()
        tenants = Tenant.query.paginate(page=page, per_page=per_page)
        return jsonify({
            'success': True,
            'data': [t.to_dict() for t in tenants.items],
            'total': tenants.total,
            'pages': tenants.pages,
            'current_page': tenants.page
        })
    
    elif request.method == 'POST':
        try:
            data = validate_json()
            validate_required_fields(data, ['name', 'phone', 'email', 'unit_id', 'property_id'])
            
            # Verify property exists
            if not Property.query.get(data['property_id']):
                raise ValueError('Property does not exist')
            
            new_tenant = Tenant(
                name=data['name'],
                phone=data['phone'],
                email=data['email'],
                unit_id=data['unit_id'],
                property_id=data['property_id']
            )
            db.session.add(new_tenant)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': new_tenant.to_dict()
            }), 201
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400

@app.route('/api/tenants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'data': tenant.to_dict()
        })
    
    elif request.method == 'PUT':
        try:
            data = validate_json()
            
            if 'property_id' in data and not Property.query.get(data['property_id']):
                raise ValueError('Property does not exist')
            
            tenant.name = data.get('name', tenant.name)
            tenant.phone = data.get('phone', tenant.phone)
            tenant.email = data.get('email', tenant.email)
            tenant.unit_id = data.get('unit_id', tenant.unit_id)
            tenant.property_id = data.get('property_id', tenant.property_id)
            
            db.session.commit()
            return jsonify({
                'success': True,
                'data': tenant.to_dict()
            })
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400
    
    elif request.method == 'DELETE':
        db.session.delete(tenant)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Tenant deleted successfully'
        })

# Payment CRUD Operations
@app.route('/api/payments', methods=['GET', 'POST'])
def handle_payments():
    if request.method == 'GET':
        page, per_page = get_pagination_params()
        payments = Payment.query.paginate(page=page, per_page=per_page)
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in payments.items],
            'total': payments.total,
            'pages': payments.pages,
            'current_page': payments.page
        })
    
    elif request.method == 'POST':
        try:
            data = validate_json()
            validate_required_fields(data, ['payment_type', 'amount', 'payment_date', 'tenant_id'])
            
            # Verify tenant exists
            if not Tenant.query.get(data['tenant_id']):
                raise ValueError('Tenant does not exist')
            
            try:
                payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
            
            new_payment = Payment(
                payment_type=data['payment_type'],
                amount=data['amount'],
                payment_date=payment_date,
                tenant_id=data['tenant_id'],
                status=data.get('status', 'pending')
            )
            db.session.add(new_payment)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': new_payment.to_dict()
            }), 201
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400

@app.route('/api/payments/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_payment(id):
    payment = Payment.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'data': payment.to_dict()
        })
    
    elif request.method == 'PUT':
        try:
            data = validate_json()
            
            if 'tenant_id' in data and not Tenant.query.get(data['tenant_id']):
                raise ValueError('Tenant does not exist')
            
            if 'payment_date' in data:
                try:
                    payment.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError('Invalid date format. Use YYYY-MM-DD')
            
            payment.payment_type = data.get('payment_type', payment.payment_type)
            payment.amount = data.get('amount', payment.amount)
            payment.status = data.get('status', payment.status)
            payment.tenant_id = data.get('tenant_id', payment.tenant_id)
            
            db.session.commit()
            return jsonify({
                'success': True,
                'data': payment.to_dict()
            })
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400
    
    elif request.method == 'DELETE':
        db.session.delete(payment)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Payment deleted successfully'
        })

# Health Check
@app.route('/api/health')
def health_check():
    return jsonify({
        'success': True,
        'message': 'API is healthy',
        'status': 'running'
    })

# Database teardown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', False))