from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '35b8553e7d8a997621395bd75f4c1e31'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///previsaoligas.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from previsaoligas import routes

