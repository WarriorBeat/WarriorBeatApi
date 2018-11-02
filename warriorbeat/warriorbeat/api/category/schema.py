"""
    warriorbeat/api/category/schema.py
    Schema for Category Resource
"""


from marshmallow import Schema, fields, post_load

from warriorbeat.api.category.model import Category


class CategorySchema(Schema):
    """Category Data Schema"""
    categoryId = fields.Str(required=True)
    name = fields.Str()

    @post_load
    def make_category(self, data):
        """return category instance"""
        category = Category.create_or_retrieve(**data, schema=CategorySchema())
        return category
