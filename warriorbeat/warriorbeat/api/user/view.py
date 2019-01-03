"""
    warriorbeat/api/user/schema.py
    Primary View for User Resource
"""

from flask_restful import Resource

from warriorbeat.api.user.model import User
from warriorbeat.api.user.schema import UserSchema
from warriorbeat.utils import (allow_relations, parse_json, retrieve_item,
                               use_schema)


class UserList(Resource):

    def get(self):
        return User.all()

    @use_schema(UserSchema(), dump=True)
    def post(self, user):
        user.create()
        return user


class UserItem(Resource):

    @retrieve_item(User, UserSchema)
    @allow_relations
    def get(self, user, data, **kwargs):
        return data

    @parse_json
    @retrieve_item(User, UserSchema)
    def patch(self, data, user, **kwargs):
        user = user.update(data)
        return user.save()

    @retrieve_item(User, UserSchema)
    def delete(self, user, **kwargs):
        user.delete()
        return '', 204
