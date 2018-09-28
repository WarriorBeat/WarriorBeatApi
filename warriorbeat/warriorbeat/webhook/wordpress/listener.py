"""
    warriorbeat/webhooks/wordpress/hook.py
    Webhook listener for wordpress
"""


from flask_restful import Resource, request
from webargs.flaskparser import use_args

from warriorbeat.utils.decorators import forward_resource
from warriorbeat.webhook.wordpress.schema import PostRequest


class HookListener(Resource):
    """
    primary hook listener for wordpress webhooks

    Determines appropriate endpoint in post and forwards 
    the request data to it

    """
    method_decorators = {
        "post": [use_args(PostRequest(context={'wp_data': request}))]}

    post_types = {
        'post': 'hook:wp:post',
        'poll': 'hook:wp:poll'
    }

    @forward_resource()
    def post(self, args):
        post_data = args['post']
        url_type = self.post_types[post_data['type']]
        self.target = url_type
        return request.form


class PostListener(HookListener):

    def post(self, data):
        post_data = data['post']
        return post_data
