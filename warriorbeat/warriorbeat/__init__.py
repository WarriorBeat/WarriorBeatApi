# warriorbeat/__init__.py

from flask import Flask
from flask_restful import Api, Resource
from .admin.views import admin
from .api.views.feed import FeedListAPI, FeedAPI
import os

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
# API
api = Api(app)
# - Feed Api
api.add_resource(FeedListAPI, '/api/feed', endpoint='feedlist')
api.add_resource(FeedAPI, '/api/feed/<string:feedId>', endpoint='feed')
# Admin Panel
app.register_blueprint(admin, url_prefix='/admin')
