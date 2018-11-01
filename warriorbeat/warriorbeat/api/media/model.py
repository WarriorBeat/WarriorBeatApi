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

    def __init__(self, mediaId, type, source):
        self.mediaId = mediaId
        self.type = type
        self.source = source


class Image(Media):
    """Image Type Media"""

    def __init__(self, mediaId, source, title, **kwargs):
        self.credits = kwargs.get('credits', None)
        self.caption = kwargs.get('caption', None)
        self.type = 'image'
        self.title = title
        self.key = kwargs.get('key', '')
        super().__init__(mediaId, self.type, source)
        self.set_source()

    def set_source(self):
        """download image from url and set source"""
        key = self.key + slugify(self.title)
        url, file_ext = self.storage.upload_from_url(self.source, key=key)
        self.source = url
        self.key = self.storage.key + key + file_ext
        return url

    def get_source(self):
        """generate url for image"""
        url = self.storage.get_url(self.key)
        self.source = url
        self.save()
        return url


class CoverImage(Image):
    """Cover Image Media Object"""

    def __init__(self, mediaId, source, title, **kwargs):
        super().__init__(
            mediaId, source, title, **kwargs)
        self.type = 'cover-image'


class ProfileImage(Image):
    """User Profile Image Model"""

    def __init__(self, mediaId, source, title, **kwargs):
        self.key = 'profile/'
        self.title = title
        super().__init__(mediaId, source, title, key=self.key, **kwargs)
        self.type = 'profile-image'
