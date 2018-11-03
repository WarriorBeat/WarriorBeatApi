"""
    warriorbeat/api/media/schema.py
    Schema for Media Resources
"""

from marshmallow import Schema, fields, post_load

from warriorbeat.api.media.model import CoverImage, ProfileImage


class MediaSchema(Schema):
    """Base Schema for Media"""
    mediaId = fields.Str()
    type = fields.Str()
    source = fields.Str()


class ImageSchema(MediaSchema):
    """Schema for Image Type Media"""
    credits = fields.Str(required=False)
    caption = fields.Str(required=False)
    title = fields.Str()
    key = fields.Str()
    type = fields.Str(missing='image', default='image')


class CoverImageSchema(ImageSchema):
    """Cover Image Schema"""
    type = fields.Str(missing='cover-image', default='cover-image')

    @post_load
    def make_cover_image(self, data):
        """return instance of CoverImage"""
        cover_img = CoverImage(**data)
        cover_img.schema = CoverImageSchema()
        return cover_img


class ProfileImageSchema(ImageSchema):
    """Profile Image Schema"""
    class Meta:
        fields = ('title', 'source', 'mediaId', 'type')

    title = fields.Str(data_key='name')
    type = fields.Str(missing='profile-image', default='profile-image')

    @post_load
    def make_profile_image(self, data):
        profile_img = ProfileImage(**data)
        profile_img.schema = ProfileImageSchema()
        return profile_img
