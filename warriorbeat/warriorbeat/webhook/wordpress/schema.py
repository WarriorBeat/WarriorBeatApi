"""
    warriorbeat/api/schema/wordpress.py
    Data Schemas for word press
"""

import requests
from flask_marshmallow import Marshmallow
from marshmallow import fields, post_load

ma = Marshmallow()


class PostRequest(ma.Schema):
    """
    Schema for post related requests from wordpress webhook
    Used for storing all the unfiltered json data
    returned by Wordpress

    Fields:
    ----
    post: dict
        data relating to the post itself
    author: dict
        data relating to the author of the post
    media: dict
        data relating to media used in the post

    Context:
    ----
    wp_data: request object
        received webhook request object
        * required

    Deserialize (loading):
    ----
    post: dict
        extracts post ID from webhook and requests complete
        data from wordpress rest api, followed by adding
        additional meta info on the post via self.populate_meta
    author: dict
        requested via get request to href in the post reference data
    media: dict
        requested via get request to href in the post reference data

    """
    class Meta:
        strict = True
    post = fields.Dict()
    author = fields.Dict()
    media = fields.Dict()

    @post_load
    def load_post(self, data):
        """Parse new/edited/deleted post from wordpress"""
        wp_data = self.context.get('wp_data').form
        post_id = wp_data['ID']
        post_request = requests.get(
            f"http://localhost:8000/wp-json/wp/v2/posts/{post_id}")
        post_data = post_request.json()
        data['post'] = self.populate_meta(post_data)
        data['author'] = self.get_ref(post_data, 'author')
        data['media'] = self.get_ref(post_data, 'wp:featuredmedia')
        return data

    def get_ref(self, data, ref_key, ref_val='href'):
        """get reference data from a post"""
        ref = data['_links']
        item_ref = ref[ref_key][0][ref_val]
        try:
            item_request = requests.get(item_ref)
            item_data = item_request.json()
        except Exception as e:
            print(f"Request Error @ ({item_ref}): {e}")
            return item_ref
        return item_data

    def populate_meta(self, post):
        """get meta information from a post"""
        revision = self.get_ref(post, 'version-history', ref_val='count')
        post['is_new'] = False if int(revision) > 0 else True
        return post
