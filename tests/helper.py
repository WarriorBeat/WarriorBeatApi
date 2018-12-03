"""
    Helper test functions
"""

from pprint import pprint
import os

DEBUG = os.environ.get('TEST_DEBUG')


class TestPrint:
    """Provides context to test prints"""

    def __init__(self, func_name):
        self.func = func_name

    def info(self, msg):
        """Context for info prints"""
        msg = f"\n[{self.func}] (Info): {msg}"
        if DEBUG == 'True':
            print(msg)

    def data(self, context, data):
        """Context for data prints"""
        msg = f"\n[{self.func}] (Debug) {context}:"
        if DEBUG == 'True':
            print(msg)
            pprint(data)
