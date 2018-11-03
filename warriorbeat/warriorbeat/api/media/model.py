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

    def __init__(self, mediaId, source, **kwargs):
        self.mediaId = mediaId
        self.source = source
        self.type = kwargs.get('type', '')


class Image(Media):
    """Image Type Media"""

    def __init__(self, title, *args, **kwargs):
        self.credits = kwargs.get('credits', None)
        self.caption = kwargs.get('caption', None)
        self.type = kwargs.get('type', 'image')
        self.title = title
        self.key = kwargs.get('key', '')
        super().__init__(*args, **kwargs)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProfileImage(Image):
    """User Profile Image Model"""

    def __init__(self, **kwargs):
        self.key = 'profile/'
        super().__init__(key=self.key, **kwargs)
        self.title = kwargs.get('title')
        self.type = kwargs.get('type', 'profile-image')
