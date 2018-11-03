"""
    warriorbeat/api/exceptions.py
    Custom Defined Exceptions for API
"""


class APIException(Exception):
    """Exception Handler for API : Base Class"""

    def __init__(self, status, message, payload=None):
        Exception.__init__(self)
        self._status = status
        self._message = message
        self._payload = payload

    def to_dict(self):
        """generate dict with exception information"""
        report = {}
        report['message'] = self.message
        report['status'] = self._status
        return report

    @property
    def status(self):
        """status code of exception"""
        return self._status

    @property
    def message(self):
        """informative message detailing the exception"""
        return self._message

    def __str__(self):
        return self.__class__.__name__ + ': ' + self._message


class ItemAlreadyExists(APIException):
    """
    Raised when an item already exists in a database

    params:
    id: string
        id of item
    """

    def __init__(self, itemId):
        message = f"An Item with id {itemId} already exists"
        super(ItemAlreadyExists, self).__init__(409, message)
