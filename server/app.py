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


if __name__ == '__main__':
    app.run(debug=True)
