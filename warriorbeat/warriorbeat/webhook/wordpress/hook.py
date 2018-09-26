"""
    warriorbeat/webhooks/wordpress/hook.py
    Webhook for wordpress
"""

from pprint import pprint

import requests
from flask_restful import Resource, request
from marshmallow import fields
from webargs.flaskparser import use_args

from warriorbeat.webhook.wordpress import parse


class PressHook(Resource):

    def get(self):
        pass

    @use_args({"data": fields.Dict()}, locations=("wp:post",))
    def post(self, args):
        pprint(args)
        return args
