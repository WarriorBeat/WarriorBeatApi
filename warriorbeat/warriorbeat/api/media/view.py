"""
    warriorbeat/api/media/view.py
    View for Media Resources
"""


from flask_restful import Resource

from warriorbeat.api.media.model import Media
from warriorbeat.api.media.schema import CoverImageSchema
from warriorbeat.utils import use_schema


class MediaList(Resource):
    def get(self):
        return Media.all()

    @use_schema(CoverImageSchema(), dump=True)
    def post(self, media):
        media.save()
        return media
