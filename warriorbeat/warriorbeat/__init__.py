"""
    warriorbeat/app.py
    Entry file for WarriorBeatApi
    Setup for flask, api, marshmallow, and other items
"""

from flask import Flask, jsonify
from flask_restful import Api
from .api.middleware import HTTPMethodOverrideMiddleware
from .api.root.view import Root
from .api.author.view import AuthorList, AuthorItem
from .api.post.view import PostList, PostItem
from .api.media.view import MediaList, MediaItem
from .api.user.view import UserList, UserItem
from .api.user.feedback.view import UserFeedbackList, UserFeedbackItem
from .api.category.view import CategoryList, CategoryItem
from .api.poll.view import PollList, PollItem
from .exceptions import ItemAlreadyExists
import pkg_resources
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import os


# Init Sentry
if os.environ.get('FLASK_TESTING') != 'True':
    version = pkg_resources.require("warriorbeat")[0].version
    sentry_sdk.init(
        dsn="https://9c5dbdae23c4481ab38987b2069d3fe5@sentry.io/1358208",
        integrations=[FlaskIntegration()],
        release=f"warriorbeatapi@{version}"
    )


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('warriorbeat.config')
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
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
rest.add_resource(UserList, '/api/users', endpoint='users')
rest.add_resource(UserItem, '/api/users/<int:userId>', endpoint='user')
rest.add_resource(UserFeedbackList, '/api/user/feedback',
                  endpoint='feedback')
rest.add_resource(UserFeedbackItem, '/api/user/feedback/<string:feedbackId>',
                  endpoint='feedback_item')
# Category Resource
rest.add_resource(CategoryList, '/api/categories', endpoint='categories')
rest.add_resource(
    CategoryItem, '/api/categories/<int:categoryId>', endpoint='category')
# Poll Resource
rest.add_resource(PollList, '/api/polls', endpoint='polls')
rest.add_resource(PollItem, '/api/polls/<int:pollId>', endpoint='poll')

# Error Handlers


@app.errorhandler(ItemAlreadyExists)
def handle_item_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status
    return response
