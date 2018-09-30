"""
    Helper test functions
"""

from pprint import pprint


class TestPrint:
    """Provides context to test prints"""

    def __init__(self, func_name):
        self.func = func_name

    def info(self, msg):
        """Context for info prints"""
        msg = f"\n[{self.func}] (Info): {msg}"
        print(msg)

    def data(self, context, data):
        """Context for data prints"""
        msg = f"\n[{self.func}] (Debug) {context}:"
        print(msg)
        pprint(data)
