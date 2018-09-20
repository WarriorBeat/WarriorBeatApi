# warriorbeat/__init__.py

import os
from flask import Flask, jsonify
from flask_restful import Api, Resource, abort
from flask_marshmallow import Marshmallow
from .admin.views import admin
from .api.views.feed import FeedAPI, FeedListAPI
from .api.exceptions import ItemAlreadyExists

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
# Marshmallow
ma = Marshmallow(app)
# API
rest = Api(app)
# - Feed Api
rest.add_resource(FeedListAPI, '/api/feed', endpoint='feedlist')
rest.add_resource(FeedAPI, '/api/feed/<string:feedId>', endpoint='feed')
# Admin Panel
app.register_blueprint(admin, url_prefix='/admin')

# Error Handlers


@app.errorhandler(ItemAlreadyExists)
def handle_item_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status
    return response


__all__ = ["app", "rest", "ma"]
