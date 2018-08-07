from flask import Flask
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['NEO4J_USER'] = os.environ['NEO4J_USER']
app.config['NEO4J_PASSWORD'] = os.environ['NEO4J_PASSWORD']

bootstrap = Bootstrap(app)

from app import routes
