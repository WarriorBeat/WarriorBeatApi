"""
    Setup File for Tests
"""

import decimal
import io
import json
import os
import unittest

import boto3

from helper import TestPrint

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
        'bucket_name': 'media-bucket-dev',
        'parent_key': 'media/'
    }
}


class ApiTestCase(unittest.TestCase):
    """
    Parent Test Case
    Setup Local DynamoDB Tables and S3 Buckets
    """

    def setUp(self):
        """create test tables and buckets"""
        t = TestPrint('Test Setup')
        dynamodb = boto3.resource(
            'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
        self.s3bucket = boto3.resource(
            's3', region_name='localhost', endpoint_url='http://localhost:9000', aws_access_key_id='accessKey1', aws_secret_access_key='verySecretKey1')
        self.s3client = boto3.client('s3', region_name='localhost',
                                     endpoint_url='http://localhost:9000',
                                     aws_access_key_id='accessKey1', aws_secret_access_key='verySecretKey1')
        t.info(f'Current Dir: {os.getcwd()}')

        def create_table(table):
            new_table = dynamodb.create_table(
                TableName=f"{table['table_name']}",
                KeySchema=[
                    {
                        'AttributeName': f"{table['primary_key']}",
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': f"{table['primary_key']}",
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            t.info(f"{table['table_name']} Status: {new_table.table_status}")
            return new_table

        def create_bucket(bucket):
            t.data('Creating Bucket', bucket)
            _bucket = self.s3client.create_bucket(
                Bucket=bucket['bucket_name'], ACL='public-read')
            bucket = self.s3bucket.Bucket(bucket['bucket_name'])
            return bucket

        self.author_table = create_table(TABLES['author'])
        self.post_table = create_table(TABLES['post'])
        self.media_table = create_table(TABLES['media'])
        self.media_bucket = create_bucket(BUCKETS['media'])
        resp = self.s3client.list_buckets()
        buckets = [bucket['Name'] for bucket in resp['Buckets']]
        t.data('Media Bucket', self.media_bucket)
        t.data('S3 Buckets', buckets)

    def tearDown(self):
        """cleanup tables and buckets"""
        t = TestPrint('TEARDOWN')
        self.author_table.delete()
        self.post_table.delete()
        self.media_table.delete()
        t.info('Testing Databases Deleted.')
        self.media_bucket.objects.all().delete()
        self.media_bucket.delete()
        t.info('Test Buckets Deleted.')

    def test_s3_bucket(self):
        """Test Local S3 Bucket"""
        t = TestPrint('test_s3_bucket')
        sample_file = 'tests/sample_author.json'
        sample_data = open(sample_file, 'r')
        expected = json.load(sample_data)
        self.media_bucket.upload_file(sample_file, 'tests/sample_author.json')
        tmpdata = io.BytesIO()
        self.media_bucket.download_fileobj(
            'tests/sample_author.json', tmpdata)
        down = json.loads(tmpdata.getvalue().decode("utf-8"))
        t.data('Expected Data', expected)
        t.data('Downloaded Data', down)
        self.assertEqual(expected, down)

    def upload_sample_author(self):
        t = TestPrint('Upload Sample Author')
        with open("tests/sample_author.json") as sample_data:
            authors = json.load(sample_data, parse_float=decimal.Decimal)
            t.data('Author Sample Data', authors)
            test_author = authors[0]
            for author in authors:
                t.info(f"Adding Author: {author['name']}")
                self.author_table.put_item(
                    Item={
                        'authorId': author['authorId'],
                        'name': author['name'],
                        'posts': author['posts'],
                        'title': author['title'],
                        'avatar': author['avatar'],
                        'description': author['description']
                    }
                )
        _resp = self.author_table.get_item(
            Key={
                'authorId': test_author['authorId']
            }
        )
        resp = _resp['Item']
        t.data('Get Item Response', resp)
        t.data('Test Assert Data', test_author)
        self.assertDictEqual(resp, test_author)

    def make_db_test(self, test_print, table, key):
        """queries database and returns data"""
        t = test_print
        _resp = table.get_item(Key=key)
        try:
            resp = _resp['Item']
        except KeyError:
            self.fail(
                f'[{test_print.func}] {list(key.keys())[0]} not found in database!')
        t.data('Resp Data', resp)
        return resp


if __name__ == '__main__':
    unittest.main()
