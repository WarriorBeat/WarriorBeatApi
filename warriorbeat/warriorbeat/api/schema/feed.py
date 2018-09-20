"""
    warriorbeat/api/schema/feed.py
    Data Schemas for FeedAPI
"""

from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import Hyperlinks, AbsoluteUrlFor
from marshmallow import fields, pre_dump, pre_load
from slugify import slugify


ma = Marshmallow()


class FeedSchema(ma.Schema):
    class Meta:
        strict = True
    feedId = fields.String()
    title = fields.String()
    author = fields.String()
    body = fields.String()
    cover_img = fields.String()
    ref = Hyperlinks({
        'self': AbsoluteUrlFor('feed', feedId='<feedId>'),
        'all': AbsoluteUrlFor('feedlist')
    })

    @pre_load
    def generate_id(self, in_data):
        in_data['feedId'] = slugify(in_data['title'], to_lower=True)
        return in_data
