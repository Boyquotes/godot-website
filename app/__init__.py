import os
from flask import Flask, jsonify
from flask_bootstrap import Bootstrap
from flask_simplelogin import SimpleLogin
from app import users


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['NEO4J_USER'] = os.environ['NEO4J_USER']
app.config['NEO4J_PASSWORD'] = os.environ['NEO4J_PASSWORD']
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config['JSON_AS_ASCII'] = False

SimpleLogin(app, login_checker=users.is_valid_user)
bootstrap = Bootstrap(app)
from app import routes
