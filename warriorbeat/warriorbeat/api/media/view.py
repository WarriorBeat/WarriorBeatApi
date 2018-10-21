"""
    warriorbeat/api/media/view.py
    View for Media Resources
"""


from flask_restful import Resource, request

from warriorbeat.api.media.model import Media
from warriorbeat.api.media.schema import CoverImageSchema


class MediaList(Resource):
    def get(self):
        return Media.all()

    def post(self):
        try:
            media = CoverImageSchema().load(request.json)
        except Exception:
            media = CoverImageSchema().loads(request.json)
        media.save()
        data = CoverImageSchema().dumps(media)
        return data
