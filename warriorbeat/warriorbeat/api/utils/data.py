"""
    warriorbeat/api/utils/data.py
    Data Handlers
"""

import os

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

# Environment Variables
TABLES = {
    'feed': os.environ['FEED_TABLE']
}
BUCKETS = {
    'feed': 'feed-bucket'
}


class DynamoDB:
    """
    AWS Boto3 DynamoDB
    Handles transactions with database

    params:
    table_name: string
        name of table to access
    """

    def __init__(self, table_name):
        self.dynamodb = boto3.resource(
            'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
        self.table = self.dynamodb.Table(table_name)

    def add_item(self, item):
        """adds item to database"""
        self.table.put_item(Item=item)
        return item

    def get_item(self, id):
        """retrieves an item item from database"""
        try:
            resp = self.table.get_item(Key={
                'feedId': id
            })
            return resp.get('Item')
        except ClientError as e:
            print(e)
            return None

    def exists(self, id):
        """checks if an item exists in the database"""
        return False if self.get_item(id) is None else True

    @property
    def all(self):
        """list all items in the database table"""
        resp = self.table.scan()
        items = resp["Items"]
        return items


class S3Storage:
    """
    AWS S3 Bucket
    Handles transactions with s3 Buckets

    params:
    bucket_name: string
        name of bucket to access
    """

    def __init__(self, bucket_name):
        self.endpoint = "http://localhost:9000"
        self.s3bucket = boto3.resource(
            's3', region_name='localhost', endpoint_url=self.endpoint)
        self.bucket_name = bucket_name
        self.storage = self.s3bucket.Bucket(self.bucket_name)
        self.key = ''

    def get_uri(self, key):
        """generates uri where the image is hosted"""
        url = self.endpoint + f"/{self.bucket_name + '/' + key}"
        return url

    def upload(self, path, key=None):
        """uploads a file to the s3 bucket"""
        if key:
            self.storage.upload_file(path, key)
            return self.get_uri(key)
        else:
            self.storage.upload_file(path, self.key)
            return self.get_uri(self.key)
