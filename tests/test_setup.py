"""
    Setup File for Tests
"""

import unittest
from helper import TestPrint
import boto3
import requests
import json
import os
import decimal

TABLES = {
    'author': {
        'table_name': 'author-table-dev',
        'primary_key': 'authorId'
    },
    'post': {
        'table_name': 'post-table-dev',
        'primary_key': 'postId'
    }
}


class ApiTestCase(unittest.TestCase):
    """
    Parent Test Case
    Setup Local DynamoDB Tables
    """

    def setUp(self):
        t = TestPrint('Test Setup')
        dynamodb = boto3.resource(
            'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
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

        self.author_table = create_table(TABLES['author'])
        self.post_table = create_table(TABLES['post'])

    def tearDown(self):
        t = TestPrint('TEARDOWN')
        self.author_table.delete()
        self.post_table.delete()
        t.info('Testing Databases Deleted.')

    def test_sample_author(self):
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
        assert resp == test_author


if __name__ == '__main__':
    unittest.main()
