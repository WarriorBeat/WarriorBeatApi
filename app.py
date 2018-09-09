import os
import json

import boto3
from flask import Flask, jsonify, request


app = Flask(__name__)

FEED_TABLE = os.environ['FEED_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client('dynamodb', region_name='localhost',
                          endpoint_url='http://localhost:8000')
else:
    client = boto3.client('dynamodb')


@app.route("/")
def main():
    return jsonify({
        'IS_OFFLINE': IS_OFFLINE
    })


@app.route("/feed/<string:feed_id>")
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
        'name': item.get('name').get('S')
    })


@app.route("/feed", methods=["POST"])
def create_feed():
    feed_id = request.json.get('feedId')
    name = request.json.get('name')
    if not feed_id or not name:
        return jsonify({
            'error': 'Please provide feedId and name'
        }), 400

    resp = client.put_item(
        TableName=FEED_TABLE,
        Item={
            'feedId': {'S': feed_id},
            'name': {'S': name}
        }
    )
    return jsonify({
        'feedId': feed_id,
        'name': name
    })
