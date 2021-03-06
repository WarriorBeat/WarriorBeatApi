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
        'table_name': 'author-table',
        'primary_key': 'authorId'
    },
    'post': {
        'table_name': 'post-table',
        'primary_key': 'postId'
    },
    'media': {
        'table_name': 'media-table',
        'primary_key': 'mediaId'
    },
    'feedback': {
        'table_name': 'user-feedback-table',
        'primary_key': 'feedbackId'
    },
    'category': {
        'table_name': 'category-table',
        'primary_key': 'categoryId'
    },
    'poll': {
        'table_name': 'poll-table',
        'primary_key': 'pollId'
    },
    'user': {
        'table_name': 'user-table',
        'primary_key': 'userId'
    }
}

BUCKETS = {
    'media': {
        'bucket_name': 'media-bucket',
        'parent_key': 'media/'
    }
}

# Environment Variables
TESTING = os.environ['FLASK_TESTING']
AWS_DEV = os.environ['AWS_DEV']


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
        _tname = self.table['table_name']
        self.table['table_name'] = _tname if AWS_DEV != 'True' else _tname + '-dev'
        self.db = self.dynamodb.Table(self.table['table_name'])

    def clean_item(self, item):
        """prepare item for database insertion"""
        clean = item.copy()
        for k, v in item.items():
            if type(v) is str and len(v) <= 0:
                clean.pop(k)
        return clean

    def add_item(self, item):
        """adds item to database"""
        item = self.clean_item(item)
        self.db.put_item(Item=item)
        return item

    def delete_item(self, itemId):
        """deletes item from database"""
        self.db.delete_item(Key={
            self.table['primary_key']: itemId
        })
        return itemId

    def get_item(self, itemId):
        """retrieves an item from database"""
        try:
            resp = self.db.get_item(Key={
                self.table['primary_key']: itemId
            })
            return resp.get('Item')
        except ClientError as e:
            print(e)
            return None

    def exists(self, itemId):
        """checks if an item exists in the database"""
        item = self.get_item(itemId)
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

    FILE_EXTENSIONS = {
        "image/jpeg": ".jpeg",
        "image/png": ".png"
    }

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
        self.bucket['bucket_name'] = self.bucket['bucket_name'] if AWS_DEV != 'True' else self.bucket['bucket_name'] + '-dev'
        self.storage = self.s3bucket.Bucket(self.bucket['bucket_name'])
        self.key = self.bucket['parent_key']

    def get_url(self, key, **kwargs):
        """generates url where the image is hosted"""
        aws_root = "https://s3.amazonaws.com"
        if TESTING == 'True':
            aws_root = "http://localhost:9000"
        url = f"{aws_root}/{self.bucket['bucket_name']}/{key}"
        return url

    def upload(self, path, key=None):
        """uploads a file to the s3 bucket"""
        if key:
            key = self.key + key
            self.storage.upload_file(path, key, ACL='public-read')
            return self.get_url(key)
        else:
            self.storage.upload_file(path, self.key, ACL='public-read')
            return self.get_url(self.key)

    def upload_obj(self, obj: tuple, key=''):
        """upload file object"""
        _key = self.key + key + obj[1]
        self.storage.put_object(Key=_key, Body=obj[0], ACL='public-read')
        return self.get_url(_key)

    def upload_from_url(self, url, **kwargs):
        """upload file from url"""
        img_stream = requests.get(url, stream=True)
        content_type = img_stream.headers.get('content-type', 'image/jpeg')
        file_ext = self.FILE_EXTENSIONS[content_type]
        img_obj = img_stream.raw
        img_data = img_obj.read()
        return (self.upload_obj((img_data, file_ext), **kwargs), file_ext)
