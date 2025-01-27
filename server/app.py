from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import migrate
from serializer import Serializer