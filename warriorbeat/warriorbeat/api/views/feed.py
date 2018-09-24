"""
    warriorbeat/api/views/feed.py
    Api Handle for News Feed
"""

from flask_restful import Resource
from webargs.flaskparser import use_args

from warriorbeat.schema.feed import FeedSchema
from warriorbeat.utils.data import BUCKETS, TABLES, DynamoDB, S3Storage
from warriorbeat.utils.decorators import use_schema


class FeedListAPI(Resource):
    def __init__(self):
        self.db = DynamoDB(TABLES['feed'])
        self.storage = S3Storage(BUCKETS['feed'])
        super(FeedListAPI, self).__init__()

    @use_schema(FeedSchema(many=True))
    def get(self):
        return self.db.all

    @use_args(FeedSchema(exclude=("ref")))
    def post(self, args):
        args['cover_img'] = self.storage.upload_from_url(
            args['cover_img'], key=f"imgs/{args['feedId']}.jpg")
        return self.db.add_item(args)


class FeedAPI(Resource):
    def __init__(self):
        self.db = DynamoDB(TABLES['feed'])
        super(FeedAPI, self).__init__()

    @use_schema(FeedSchema())
    def get(self, feedId):
        item = self.db.get_item(feedId)
        return item
