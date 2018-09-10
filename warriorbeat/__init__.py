# warriorbeat/__init__.py

from flask import Flask
from .api.views import api
from .admin.views import admin

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
# API
app.register_blueprint(api)
# Admin Panel
app.register_blueprint(admin, url_prefix='/admin')
