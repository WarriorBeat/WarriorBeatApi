"""
    warriorbeat/api/model.py
    Base Classes for Api Models
"""

from warriorbeat.utils import deep_merge_dicts


class ResourceModel:
    """Base Class for Resource Models"""
    db = None
    storage = None
    identity = None

    def __init__(self, *args, **kwargs):
        self.schema = None

    @classmethod
    def create_or_update(cls, **kwargs):
        """return resource if it exists, otherwise create one"""
        itemId = kwargs.get(cls.identity)
        item = cls.db.exists(itemId)
        if not item:
            return cls(**kwargs)
        item = {**item, **kwargs}
        return cls(**item)

    @classmethod
    def retrieve(cls, identity, schema=None, instance=False):
        """retrieve item from database by id"""
        item = cls.db.get_item(str(identity))
        if item is None:
            return None
        if schema or instance:
            item = cls(**item)
            item.schema = schema() if schema else None
            return item
        return item

    @classmethod
    def all(cls):
        """return all items"""
        data = cls.db.all
        return data

    def update(self, data):
        """merge item with new data"""
        item_id = getattr(self, self.identity)
        item_data = self.db.get_item(item_id)
        deep_merge_dicts(item_data, data)
        updated_item = self.schema.load(item_data)
        return updated_item

    def save(self):
        """save item to database"""
        dumped = self.schema.dump(self)
        self.db.add_item(dumped)
        return dumped

    def delete(self):
        """delete item from database"""
        itemId = getattr(self, self.identity)
        self.db.delete_item(itemId)
        return itemId

    def create(self):
        """create item from model"""
        return self.save()
