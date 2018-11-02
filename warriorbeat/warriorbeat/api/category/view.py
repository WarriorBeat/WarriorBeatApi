"""
    warriorbeat/api/category/view.py
    View for Category Resource
"""

from flask_restful import Resource

from warriorbeat.api.category.model import Category
from warriorbeat.api.category.schema import CategorySchema
from warriorbeat.utils import use_schema


class CategoryList(Resource):
    def get(self):
        return Category.all()

    @use_schema(CategorySchema(), dump=True)
    def post(self, category):
        return category


class CategoryItem(Resource):
    def get(self, categoryId):
        category = Category.retrieve(categoryId)
        return category
