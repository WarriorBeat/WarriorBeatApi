"""
    warriorbeat/api/utils/data.py
    Data Handlers
"""


import boto3
import requests
from botocore.exceptions import ClientError


# Environment Variables
TABLES = {
    'feed': 'feed-table-dev'
}
BUCKETS = {
    'feed': 'feed-bucket-dev'
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
        self.dynamodb = boto3.resource('dynamodb')
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
        self.s3bucket = boto3.resource('s3')
        self.s3client = boto3.client('s3')
        self.bucket_name = bucket_name
        self.storage = self.s3bucket.Bucket(self.bucket_name)
        self.key = ''

    def get_url(self, key, **kwargs):
        """generates url where the image is hosted"""
        method = kwargs.get('method', 'get_object')
        expire = kwargs.get('expire', 0)
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
            self.storage.upload_file(path, key)
            return self.get_url(key)
        else:
            self.storage.upload_file(path, self.key)
            return self.get_url(self.key)

    def upload_obj(self, obj, key=''):
        """upload file object"""
        self.storage.put_object(Key=key, Body=obj)
        return self.get_url(key)

    def upload_from_url(self, url, **kwargs):
        """upload file from url"""
        img_stream = requests.get(url, stream=True)
        img_obj = img_stream.raw
        img_data = img_obj.read()
        return self.upload_obj(img_data, **kwargs)