from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import migrate
from serializer import Serializer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rent_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app)
serializer = Serializer()


