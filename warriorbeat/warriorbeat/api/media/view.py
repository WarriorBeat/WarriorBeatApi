"""
    warriorbeat/api/media/view.py
    View for Media Resources
"""


from flask_restful import Resource

from warriorbeat.api.media.model import Media
from warriorbeat.api.media.schema import ImageSchema
from warriorbeat.utils import parse_json, retrieve_item, use_schema


class MediaList(Resource):
    def get(self):
        return Media.all()

    @use_schema(ImageSchema(), dump=True)
    def post(self, media):
        media.set_source()
        media.save()
        return media


class MediaItem(Resource):

    @retrieve_item(Media)
    def get(self, media, **kwargs):
        return media

    @parse_json
    @retrieve_item(Media, ImageSchema)
    def patch(self, data, media, **kwargs):
        media = media.update(data)
        media.set_source()
        return media.save()

    @retrieve_item(Media, ImageSchema)
    def delete(self, media, **kwargs):
        media.delete()
        return '', 204
