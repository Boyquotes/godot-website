import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_simplelogin import SimpleLogin
from app import users
from app import routes

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['NEO4J_USER'] = os.environ['NEO4J_USER']
app.config['NEO4J_PASSWORD'] = os.environ['NEO4J_PASSWORD']


SimpleLogin(app, login_checker=users.is_valid_user)
bootstrap = Bootstrap(app)

