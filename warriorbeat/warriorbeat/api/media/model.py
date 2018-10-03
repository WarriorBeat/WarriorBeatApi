"""
    warriorbeat/api/media/model.py
    Models for Media Resources
"""

import requests
from warriorbeat.utils.data import S3Storage
from slugify import slugify


class Media(object):
    """Base Class for Media resource"""
    storage = S3Storage('media')

    def __init__(self, mediaId, type, source):
        self.mediaId = mediaId
        self.type = type
        self.source = source
        self.schema = None


class Image(Media):
    """Image Type Media"""

    def __init__(self, mediaId, source, title, **kwargs):
        self.credits = kwargs.get('credits', '')
        self.caption = kwargs.get('caption', '')
        self.type = 'image'
        self.title = title
        self.key = ''
        super(Image, self).__init__(mediaId, self.type, source)
        self.set_source()

    def set_source(self):
        """download image from url and set source"""
        key = slugify(self.title)
        url = self.storage.upload_from_url(self.source, key=key)
        self.source = url
        self.key = self.storage.key + key
        return url

    def get_source(self):
        """generate url for image"""
        url = self.storage.get_url(self.key)
        self.source = url
        return url


class CoverImage(Image):
    """Cover Image Media Object"""

    def __init__(self, mediaId, source, title, **kwargs):
        super(CoverImage, self).__init__(
            mediaId, source, title, **kwargs)
        self.type = 'cover-image'
