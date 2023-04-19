from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key' # replace with your own secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TasteMateDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from TasteMate.Models import Users

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

from TasteMate import Routes