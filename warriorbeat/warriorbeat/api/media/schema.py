"""
    warriorbeat/api/media/schema.py
    Schema for Media Resources
"""

from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import AbsoluteUrlFor, Hyperlinks
from marshmallow import fields, post_load

from warriorbeat.api.media.model import CoverImage

ma = Marshmallow()


class CoverImageSchema(ma.Schema):
    """Cover Image Schema"""
    class Meta:
        strict = True
    mediaId = fields.Str()
    source = fields.Str()
    credits = fields.Str()
    caption = fields.Str()
    title = fields.Str()
    type = fields.Str()
    key = fields.Str()

    @post_load
    def make_cover_image(self, data):
        cover_img = CoverImage(**data)
        cover_img.schema = CoverImageSchema()
        return cover_img
