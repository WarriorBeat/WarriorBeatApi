"""
    warriorbeat/api/root/view.py
    Root Resource for Root of API
"""

from flask_restful import Resource


class Root(Resource):
    def get(self):
        return {
            'body': 'WarriorBeatApi'
        }
