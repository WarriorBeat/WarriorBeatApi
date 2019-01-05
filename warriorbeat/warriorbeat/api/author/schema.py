"""
    warriorbeat/api/author/schema.py
    Schema for Author Resource
"""

from marshmallow import Schema, fields, post_load

from warriorbeat.api.author.model import Author


class AuthorSchema(Schema):
    """Author Schema"""
    authorId = fields.Str(required=True)
    name = fields.Str()
    profile_image = fields.Pluck('ImageSchema', 'mediaId')
    posts = fields.Pluck('ArticleSchema', 'postId', many=True)
    title = fields.Method('author_role', deserialize='get_author_role')
    description = fields.Str(
        required=False, allow_none=True, default='Staff Member')
    post_count = fields.Str()
    staff_year = fields.Str()
    grade_year = fields.Str()

    def author_role(self, obj):
        """return author role"""
        return obj.title

    def get_author_role(self, title):
        """parse author custom role out of standard ones"""
        if type(title) is str:
            return title
        ignored_roles = ['administrator', 'author', 'contributor',
                         'customer', 'editor', 'shop_manager', 'subscriber']
        titles = [t for t in title if not t in ignored_roles]
        for t in titles:
            t = t.split('_')
            t = [i.capitalize() for i in t]
            title = " ".join(t)
        return title

    @post_load
    def make_author(self, data):
        author = Author.create_or_update(**data)
        author.schema = AuthorSchema()
        return author
