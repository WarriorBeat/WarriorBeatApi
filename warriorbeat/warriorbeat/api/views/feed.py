# warriorbeat/api/views/feed.py
# Api Handle for News Feed

from autopep8 import parse_args
from flask_restful import Api, Resource, reqparse
from warriorbeat.api.utils.data import DynamoDB, S3Storage, TABLES, BUCKETS


class FeedListAPI(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument(
            'title', type=str, location='json', required=True, help='No title provided!')
        self.parse.add_argument('author', type=str, location='json')
        self.parse.add_argument('body', type=str, location='json')
        self.parse.add_argument('feedId', type=str, location='json')
        self.parse.add_argument('cover_img', type=str, location='json')
        self.db = DynamoDB(TABLES['feed'])
        self.storage = S3Storage(BUCKETS['feed'])
        super(FeedListAPI, self).__init__()

    def get(self):
        return self.db.all

    def post(self):
        args = self.parse.parse_args()
        url = self.storage.upload(
            args['cover_img'], key=f"imgs/{args['feedId']}.jpg")
        args['cover_img'] = url
        self.db.add_item(args)
        return args


class FeedAPI(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument(
            'feedId', type=str, location='json', required=True, help='No ID provided!')
        self.db = DynamoDB(TABLES['feed'])
        super(FeedAPI, self).__init__()

    def get(self, id):
        item = self.db.get_item(id)
        print(item)
        return item

    def put(self):
        pass

    def delete(self):
        pass
