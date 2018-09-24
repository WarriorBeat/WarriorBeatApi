"""
    warriorbeat/app.py
    Entry file for WarriorBeatApi
    Setup for flask, api, marshmallow, and other items
"""

from flask import Flask, jsonify
from flask_restful import Api
from flask_marshmallow import Marshmallow
from .api.views.feed import FeedAPI, FeedListAPI
from .exceptions import ItemAlreadyExists

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('warriorbeat.config')

try:
    app.config.from_pyfile('config.py')
except FileNotFoundError:
    pass

# Marshmallow
ma = Marshmallow(app)
# API
rest = Api(app)
# - Feed Api
rest.add_resource(FeedListAPI, '/api/feed', endpoint='feedlist')
rest.add_resource(FeedAPI, '/api/feed/<string:feedId>', endpoint='feed')


# Error Handlers
@app.errorhandler(ItemAlreadyExists)
def handle_item_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status
    return response
