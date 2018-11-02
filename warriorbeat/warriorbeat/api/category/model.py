"""
    warriorbeat/api/category/model.py
    Model for Category Resource
"""

from warriorbeat.api.model import ResourceModel
from warriorbeat.utils import DynamoDB


class Category(ResourceModel):
    """Model For Post Categories"""
    db = DynamoDB('category')
    identity = 'categoryId'

    def __init__(self, categoryId, **kwargs):
        self.categoryId = categoryId
        self.name = kwargs.get('name')
        self.schema = kwargs.get('schema')
        if not self.db.exists(self.categoryId):
            self.save()
