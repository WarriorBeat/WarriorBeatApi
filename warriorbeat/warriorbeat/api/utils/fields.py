"""
    warriorbeat/api/utils/fields.py
    Extra Marshal Fields
"""
from flask_restful import fields
from slugify import slugify
from datetime import datetime


class SlugifyItem(fields.Raw):
    """
    Custom Marshall Field
    Returns slugified version of value
    """

    def format(self, value):
        return slugify(value, to_lower=True)


class ReadDateItem(fields.Raw):
    """
    Custom Marshall Field
    Returns reader friendly date
    """

    def format(self, value):
        date = datetime.strptime(value, '%Y-%m-%d T %H:%M:%S')
        return date.strftime('%m/%d/%Y')
