"""
    warriorbeat/api/media/schema.py
    Schema for Media Resources
"""

from marshmallow import Schema, fields, post_load

from warriorbeat.api.media.model import Image


class MediaSchema(Schema):
    """Base Schema for Media"""
    mediaId = fields.Str()
    type = fields.Str()
    source = fields.Str()


class ImageSchema(MediaSchema):
    """Schema for Image Type Media"""
    credits = fields.Str()
    caption = fields.Str()
    title = fields.Str()
    key = fields.Str()
    url = fields.Str()
    type = fields.Str(missing='image', default='image')

    @post_load
    def make_image(self, data):
        """return image instance"""
        image = Image.create_or_update(**data)
        image.schema = ImageSchema()
        return image
