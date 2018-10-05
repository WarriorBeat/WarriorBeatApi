"""
    warriorbeat/api/utils/data.py
    Data Handlers
"""


import os

import boto3
import requests
from botocore.exceptions import ClientError

# Connection Info
TABLES = {
    'author': {
        'table_name': 'author-table-dev',
        'primary_key': 'authorId'
    },
    'post': {
        'table_name': 'post-table-dev',
        'primary_key': 'postId'
    },
    'media': {
        'table_name': 'media-table-dev',
        'primary_key': 'mediaId'
    }
}

BUCKETS = {
    'media': {
        'bucket_name': 'media-bucket',
        'parent_key': 'media/'
    }
}

# Testing Data
TESTING = os.environ['FLASK_TESTING']


class DynamoDB:
    """
    AWS Boto3 DynamoDB
    Handles transactions with database

    params:
    table_name: string
        name of table to access
    """

    def __init__(self, table):
        if TESTING == 'True':
            self.dynamodb = boto3.resource(
                'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
        else:
            self.dynamodb = boto3.resource('dynamodb')
        self.table = TABLES[table]
        self.db = self.dynamodb.Table(self.table['table_name'])

    def add_item(self, item):
        """adds item to database"""
        self.db.put_item(Item=item)
        return item

    def get_item(self, id):
        """retrieves an item item from database"""
        try:
            resp = self.db.get_item(Key={
                self.table['primary_key']: id
            })
            return resp.get('Item')
        except ClientError as e:
            print(e)
            return None

    def exists(self, id):
        """checks if an item exists in the database"""
        item = self.get_item(id)
        return False if item is None else item

    @property
    def all(self):
        """list all items in the database table"""
        resp = self.db.scan()
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

    def __init__(self, bucket):
        if TESTING == 'True':
            self.s3bucket = boto3.resource(
                's3', region_name='localhost', endpoint_url='http://localhost:9000', aws_access_key_id='accessKey1', aws_secret_access_key='verySecretKey1')
            self.s3client = boto3.client(
                's3', region_name='localhost', endpoint_url='http://localhost:9000', aws_access_key_id='accessKey1', aws_secret_access_key='verySecretKey1')
        else:
            self.s3bucket = boto3.resource('s3')
            self.s3client = boto3.client('s3')
        self.bucket = BUCKETS[bucket]
        self.bucket_name = self.bucket['bucket_name']
        self.storage = self.s3bucket.Bucket(self.bucket_name)
        self.key = self.bucket['parent_key']

    def get_url(self, key, **kwargs):
        """generates url where the image is hosted"""
        method = kwargs.get('method', 'get_object')
        expire = kwargs.get('expire', 604800)
        url = self.s3client.generate_presigned_url(
            ClientMethod=method,
            ExpiresIn=expire,
            Params={
                'Bucket': self.bucket_name,
                'Key': key
            }
        )
        return url

    def upload(self, path, key=None):
        """uploads a file to the s3 bucket"""
        if key:
            key = self.key + key
            self.storage.upload_file(path, key)
            return self.get_url(key)
        else:
            self.storage.upload_file(path, self.key)
            return self.get_url(self.key)

    def upload_obj(self, obj, key=''):
        """upload file object"""
        _key = self.key + key
        self.storage.put_object(Key=_key, Body=obj)
        return self.get_url(_key)

    def upload_from_url(self, url, **kwargs):
        """upload file from url"""
        img_stream = requests.get(url, stream=True)
        img_obj = img_stream.raw
        img_data = img_obj.read()
        return self.upload_obj(img_data, **kwargs)
