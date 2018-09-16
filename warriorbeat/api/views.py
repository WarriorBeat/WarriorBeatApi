# warriorbeat/api/views.py


import json
import os
import boto3

from flask import Blueprint, Flask, jsonify, request


api = Blueprint('api', __name__, template_folder='templates',
                static_folder='static')


FEED_TABLE = os.environ['FEED_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client('dynamodb', region_name='localhost',
                          endpoint_url='http://localhost:8000')
    s3 = boto3.client(
        's3', region_name='localhost', endpoint_url='http://localhost:9000')
else:
    client = boto3.client('dynamodb')
    # TODO: Setup AWS S3 Resource
dynamodb = boto3.resource('dynamodb')


@api.route("/")
def main():
    return jsonify({
        'IS_OFFLINE': IS_OFFLINE
    })


@api.route("/feed/<string:feed_id>")
def get_feed(feed_id):
    resp = client.get_item(
        TableName=FEED_TABLE,
        Key={
            'feedId': {'S': feed_id}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Feed Item does not exist.'}), 404

    return jsonify({
        'feedId': item.get('feedId').get('S'),
        'title': item.get('title').get('S'),
        'author': item.get('author').get('S'),
        'body': item.get('body').get('S'),
        'slug': item.get('slug').get('S'),
        'date': item.get('date').get('S'),
        'image': item.get('image').get('S'),
    })


@api.route("/feed", methods=["POST"])
def create_feed():
    feed_id = request.json.get('feedId')
    title = request.json.get('title')
    author = request.json.get('author')
    body = request.json.get('body')
    slug = request.json.get('slug')
    date = request.json.get('date')
    image = request.json.get('cover_img')

    if not feed_id or not title:
        return jsonify({
            'error': 'Please provide feedId and name'
        }), 400
    s3.upload_file(image, "feed-bucket", f"imgs/{feed_id}.jpg")
    image_key = f"imgs/{feed_id}.jpg"
    resp = client.put_item(
        TableName=FEED_TABLE,
        Item={
            'feedId': {'S': feed_id},
            'title': {'S': title},
            'author': {'S': author},
            'body': {'S': body},
            'slug': {'S': slug},
            'date': {'S': date},
            'image': {'S': image_key}
        }
    )
    return jsonify({
        'feedId': feed_id,
        'title': title,
        'author': author,
        'body': body,
        'slug': slug,
        'date': date,
        'image': image_key
    })
