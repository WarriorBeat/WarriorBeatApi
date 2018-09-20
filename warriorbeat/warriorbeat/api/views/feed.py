# warriorbeat/api/views/feed.py
# Api Handle for News Feed

from flask_restful import Api, Resource, reqparse, marshal_with, fields
from webargs.flaskparser import use_args
from warriorbeat.api.utils.data import DynamoDB, S3Storage, TABLES, BUCKETS
from warriorbeat.api.utils.fields import SlugifyItem, ReadDateItem
from warriorbeat.api.utils.decorators import post_modify, validate_unique
from warriorbeat.api.schema.feed import FeedSchema


class FeedListAPI(Resource):
    def __init__(self):
        self.db = DynamoDB(TABLES['feed'])
        self.storage = S3Storage(BUCKETS['feed'])
        super(FeedListAPI, self).__init__()

    def get(self):
        _schema = FeedSchema(many=True)
        items = _schema.dump(self.db.all)
        return items

    @use_args(FeedSchema(exclude=("ref")))
    def post(self, args):
        args['cover_img'] = self.storage.upload(
            args['cover_img'], key=f"imgs/{args['feedId']}.jpg")
        return self.db.add_item(args)


class FeedAPI(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument(
            'feedId', type=str, location='json', required=True, help='No ID provided!')
        self.db = DynamoDB(TABLES['feed'])
        super(FeedAPI, self).__init__()

    def get(self, feedId):
        _schema = FeedSchema()
        item = self.db.get_item(feedId)
        item = _schema.dump(item)
        return item
