"""
    warriorbeat/api/media/view.py
    View for Media Resources
"""


from flask_restful import Resource, request
from warriorbeat.api.media.schema import CoverImageSchema


class MediaList(Resource):
    def get(self):
        pass

    def post(self):
        media = CoverImageSchema().loads(request.json).data
        data = CoverImageSchema().dumps(media)
        return data
