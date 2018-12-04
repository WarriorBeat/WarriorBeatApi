"""
    warriorbeat/api/media/model.py
    Models for Media Resources
"""

from slugify import slugify

from warriorbeat.api.model import ResourceModel
from warriorbeat.utils import DynamoDB, S3Storage


class Media(ResourceModel):
    """Base Class for Media resource"""
    storage = S3Storage('media')
    db = DynamoDB('media')
    identity = 'mediaId'

    def __init__(self, mediaId, **kwargs):
        self.mediaId = mediaId
        self.source = kwargs.get('source')
        self.type = kwargs.get('type', '')


class Image(Media):
    """Image Type Media"""

    def __init__(self, *args, **kwargs):
        self.credits = kwargs.get('credits', None)
        self.caption = kwargs.get('caption', None)
        self.type = kwargs.get('type', 'image')
        self.title = kwargs.get('title')
        self.key = kwargs.get('key', '')
        super().__init__(*args, **kwargs)

    def set_source(self):
        """download image from url and set source"""
        key = self.key + slugify(self.title)
        url, file_ext = self.storage.upload_from_url(self.source, key=key)
        self.source = url
        self.key = self.storage.key + key + file_ext
        return url
