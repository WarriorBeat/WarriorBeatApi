"""
    warriorbeat/api/category/view.py
    View for Category Resource
"""

from flask_restful import Resource

from warriorbeat.api.category.model import Category
from warriorbeat.api.category.schema import CategorySchema
from warriorbeat.utils import parse_json, retrieve_item, use_schema


class CategoryList(Resource):
    def get(self):
        return Category.all()

    @use_schema(CategorySchema(), dump=True, allow_many=True)
    def post(self, categories):
        categories = [c.create() for c in categories]
        return categories


class CategoryItem(Resource):

    @retrieve_item(Category)
    def get(self, category, **kwargs):
        return category

    @parse_json
    @retrieve_item(Category, CategorySchema)
    def patch(self, data, category, **kwargs):
        category = category.update(data)
        return category.save()

    @use_schema(CategorySchema(), dump=True)
    def put(self, category, **kwargs):
        category.create()
        return category

    @retrieve_item(Category, CategorySchema)
    def delete(self, category, **kwargs):
        category.delete()
        return '', 204
