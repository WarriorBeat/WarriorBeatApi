# warriorbeat/api/views/feed.py
# Api Handle for News Feed

from flask_restful import Api, Resource, reqparse, marshal_with, fields
from warriorbeat.api.utils.data import DynamoDB, S3Storage, TABLES, BUCKETS
from warriorbeat.api.utils.fields import SlugifyItem, ReadDateItem
from warriorbeat.api.utils.decorators import post_modify, validate_unique

resource_fields = {
    'feedId': fields.String,
    'title': fields.String,
    'author': fields.String,
    'body': fields.String,
    'cover_img': fields.String,
    'slug': SlugifyItem(attribute='title'),
    'uri': fields.Url('feed', absolute=True),
    'date': ReadDateItem(attribute='date')
}


class FeedListAPI(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument(
            'title', type=str, location='json')
        self.parse.add_argument('author', type=str, location='json')
        self.parse.add_argument('body', type=str, location='json')
        self.parse.add_argument('feedId', type=str, location='json')
        self.parse.add_argument('cover_img', type=str, location='json')
        self.db = DynamoDB(TABLES['feed'])
        self.storage = S3Storage(BUCKETS['feed'])
        super(FeedListAPI, self).__init__()

    @marshal_with(resource_fields)
    def get(self):
        return self.db.all

    @validate_unique('feedId')
    @post_modify(date=True)
    def post(self):
        args = self.parse.parse_args()
        args['cover_img'] = self.storage.upload(
            args['cover_img'], key=f"imgs/{args['feedId']}.jpg")
        return args, self.db.add_item


class FeedAPI(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument(
            'feedId', type=str, location='json', required=True, help='No ID provided!')
        self.db = DynamoDB(TABLES['feed'])
        super(FeedAPI, self).__init__()

    @marshal_with(resource_fields)
    def get(self, feedId):
        item = self.db.get_item(feedId)
        print(item)
        return item

    def put(self):
        pass

    def delete(self):
        pass
