"""
    warriorbeat/api/model.py
    Base Classes for Api Models
"""


class ResourceModel:
    """Base Class for Resource Models"""
    db = None
    storage = None
    identity = None

    def __init__(self, *args, **kwargs):
        self.schema = None

    @classmethod
    def create_or_retrieve(cls, **kwargs):
        """return resource if it exists, otherwise create one"""
        itemId = kwargs.get(cls.identity)
        item = cls.db.exists(itemId)
        if not item:
            return cls(**kwargs)
        return cls(**item)

    @classmethod
    def retrieve(cls, identity):
        """retrieve item from database by id"""
        item = cls.db.get_item(str(identity))
        return item

    @classmethod
    def all(cls):
        """return all items"""
        data = cls.db.all
        return data

    def save(self):
        """save item to database"""
        dumped = self.schema.dump(self)
        self.db.add_item(dumped)
