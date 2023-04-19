from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key' # replace with your own secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TasteMateDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from TasteMate import Routes