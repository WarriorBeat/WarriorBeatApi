"""
    warriorbeat/api/schema/feed.py
    Data Schemas for FeedAPI
"""

from datetime import datetime

from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import AbsoluteUrlFor, Hyperlinks
from marshmallow import fields, pre_load
from slugify import slugify

ma = Marshmallow()


class FeedSchema(ma.Schema):
    """
    Schema for de/serializiation of Feed related data

    params:
    ----
    title: string
        title of feed item
    author: string
        author of feed item
    body: string
        body of feed item
    cover_img: string (url)
        url to image, will be uploaded to s3

    serialize (dumping):
    ----
    input data
    feedId: string
        slug of title
    date: string
        creation date in '%m/%d/%Y' format (for readability)
    ref: dict
        self: string
            absolute link to self
        all: string
            absolute link to list of feeds

    deserialize (loading):
    ----
    input data
    feedId: string
        slug of title
    date: string
        creation date in '%Y-%m-%d T %H:%M:%S' format
    ref: Hyperlinks object
        self: AbsoluteUrlFor object
        all: AbsoluteUrlFor object

    """
    class Meta:
        """strict: recommended for webargs"""
        strict = True
    feedId = fields.String()
    title = fields.String()
    author = fields.String()
    body = fields.String()
    cover_img = fields.String()
    date = fields.Method('load_create_date')
    ref = Hyperlinks({
        'self': AbsoluteUrlFor('feed', feedId='<feedId>'),
        'all': AbsoluteUrlFor('feedlist')
    })

    @pre_load
    def generate_id(self, in_data):
        """generate slugified ID from title"""
        in_data['feedId'] = slugify(in_data['title'])
        return in_data

    @pre_load
    def get_create_date(self, in_data):
        """get creation date"""
        now = datetime.now()
        in_data['date'] = datetime.strftime(now, '%Y-%m-%d T %H:%M:%S')
        return in_data

    def load_create_date(self, obj):
        """load creation date"""
        date = datetime.strptime(obj['date'], '%Y-%m-%d T %H:%M:%S')
        return date.strftime('%m/%d/%Y')
