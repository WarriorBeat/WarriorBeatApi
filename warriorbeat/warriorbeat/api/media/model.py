"""
    warriorbeat/api/media/model.py
    Models for Media Resources
"""


class Media(object):
    """Base Class for Media resource"""

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
        super(Image, self).__init__(mediaId, self.type, source)


class CoverImage(Image):
    """Cover Image Media Object"""

    def __init__(self, mediaId, source, title, **kwargs):
        super(CoverImage, self).__init__(
            mediaId, source, title, **kwargs)
        self.type = 'cover-image'
