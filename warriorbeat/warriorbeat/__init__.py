"""
    warriorbeat/app.py
    Entry file for WarriorBeatApi
    Setup for flask, api, marshmallow, and other items
"""

from flask import Flask, jsonify
from flask_restful import Api
from .api.root.view import Root
from .api.author.view import AuthorList
from .api.post.view import PostList
from .api.media.view import MediaList
from .exceptions import ItemAlreadyExists

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('warriorbeat.config')

try:
    app.config.from_pyfile('config.py')
except FileNotFoundError:
    pass

# API
rest = Api(app)
# Root
rest.add_resource(Root, '/', endpoint='root')
# Author Resource
rest.add_resource(AuthorList, '/api/authors', endpoint='authors')
# Post Resource
rest.add_resource(PostList, '/api/posts', endpoint='posts')
# Media Resource
rest.add_resource(MediaList, '/api/media', endpoint='media')

# Error Handlers


@app.errorhandler(ItemAlreadyExists)
def handle_item_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status
    return response
