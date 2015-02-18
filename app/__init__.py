import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

DEV_CONFIG = 'env-config.Development'
CONFIG_FILE = os.environ.get('PRODUCTION_CONFIG', DEV_CONFIG)
app.config.from_object(CONFIG_FILE)

# DB configuration.
db = SQLAlchemy(app)

from app import views
from dbmodel import models
