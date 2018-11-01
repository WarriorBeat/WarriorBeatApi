"""
    warriorbeat/app.py
    Entry file for WarriorBeatApi
    Setup for flask, api, marshmallow, and other items
"""

from flask import Flask, jsonify
from flask_restful import Api
from .api.root.view import Root
from .api.author.view import AuthorList, AuthorItem
from .api.post.view import PostList, PostItem
from .api.media.view import MediaList, MediaItem
from .api.user.view import UserFeedbackList, UserFeedbackItem
from .exceptions import ItemAlreadyExists
from flask import Flask, jsonify
from flask_restful import Api

from warriorbeat.api.user.view import UserFeedbackList


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
rest.add_resource(AuthorItem, '/api/authors/<int:authorId>', endpoint='author')
# Post Resource
rest.add_resource(PostList, '/api/posts', endpoint='posts')
rest.add_resource(PostItem, '/api/posts/<int:postId>', endpoint='post')
# Media Resource
rest.add_resource(MediaList, '/api/media', endpoint='media')
rest.add_resource(MediaItem, '/api/media/<int:mediaId>', endpoint='media_item')
# User Resource
rest.add_resource(UserFeedbackList, '/api/user/feedback',
                  endpoint='feedback')
rest.add_resource(UserFeedbackItem, '/api/user/feedback/<string:feedbackId>',
                  endpoint='feedback_item')
# Error Handlers


@app.errorhandler(ItemAlreadyExists)
def handle_item_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status
    return response
