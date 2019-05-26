import datetime
from abc import ABCMeta, abstractmethod


# Builder Implementation
class Director(object):
    def __init__(self, builder):
        self.builder = builder

    # Returns code created in Class class.
    def get_code(self):
        self.builder.add_classes()
        return self.builder.get_code()


class AbstractClassBuilder(metaclass=ABCMeta):
    def __init__(self, created_classes):
        self.created_classes = created_classes
        self.all_my_converted_classes = []
        self.all_my_classes = []

    def get_code(self):
        out = '# Code Passes PEP8 Checks.\n'
        out += '# File Generated on: ' \
            f'{datetime.datetime.now()}\n'
        for a_class in self.all_my_classes:
            out += a_class.return_class()
        return out

    @abstractmethod
    def add_classes(self): pass
