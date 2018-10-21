"""
    warriorbeat/api/media/schema.py
    Schema for Media Resources
"""

from flask_marshmallow import Marshmallow
from marshmallow import fields, post_load

from warriorbeat.api.media.model import CoverImage, ProfileImage

ma = Marshmallow()


class MediaSchema(ma.Schema):
    """Base Schema for Media"""
    class Meta:
        strict = True
    mediaId = fields.Str()
    type = fields.Str()
    source = fields.Str()


class ImageSchema(MediaSchema):
    """Schema for Image Type Media"""
    credits = fields.Str(required=False)
    caption = fields.Str(required=False)
    title = fields.Str()
    key = fields.Str()


class CoverImageSchema(ImageSchema):
    """Cover Image Schema"""

    @post_load
    def make_cover_image(self, data):
        """return instance of CoverImage"""
        cover_img = CoverImage(**data)
        cover_img.schema = CoverImageSchema()
        return cover_img


class ProfileImageSchema(ImageSchema):
    """Profile Image Schema"""
    class Meta:
        strict = True
        fields = ('title', 'source', 'mediaId', 'type')

    title = fields.Str(load_from='name')

    @post_load
    def make_profile_image(self, data):
        profile_img = ProfileImage(**data)
        profile_img.schema = ProfileImageSchema()
        return profile_img
