# warriorbeat/api/utils/data.py
# Mixins for Data handling

import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

# Environment Variables
TABLES = {
    'feed': os.environ['FEED_TABLE']
}
BUCKETS = {
    'feed': 'feed-bucket'
}


class DynamoDB:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource(
            'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
        self.table = self.dynamodb.Table(table_name)

    def add_item(self, item):
        self.table.put_item(Item=item)
        return item

    def get_item(self, id):
        resp = self.table.get_item(Key={
            'feedId': id
        })
        return resp.get('Item')

    @property
    def all(self):
        resp = self.table.scan()
        items = resp["Items"]
        return items


class S3Storage:
    def __init__(self, bucket_name):
        self.endpoint = "http://localhost:9000"
        self.s3bucket = boto3.resource(
            's3', region_name='localhost', endpoint_url=self.endpoint)
        self.bucket_name = bucket_name
        self.storage = self.s3bucket.Bucket(self.bucket_name)
        self.key = ''

    def get_uri(self, key):
        url = self.endpoint + f"/{self.bucket_name + '/' + key}"
        return url

    def upload(self, path, key=None):
        if key:
            self.storage.upload_file(path, key)
            return self.get_uri(key)
        else:
            resp = self.storage.upload_file(path, self.key)
            return self.get_uri(self.key)
