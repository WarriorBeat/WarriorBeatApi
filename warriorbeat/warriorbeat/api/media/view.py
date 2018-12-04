"""
    warriorbeat/api/media/view.py
    View for Media Resources
"""


from flask_restful import Resource

from warriorbeat.api.media.model import Media
from warriorbeat.api.media.schema import ImageSchema
from warriorbeat.utils import use_schema


class MediaList(Resource):
    def get(self):
        return Media.all()

    @use_schema(ImageSchema(), dump=True)
    def post(self, media):
        media.set_source()
        media.save()
        return media


class MediaItem(Resource):
    def get(self, mediaId):
        media = Media.retrieve(mediaId)
        return media
