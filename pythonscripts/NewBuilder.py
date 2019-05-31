
from abc import ABCMeta, abstractmethod


# Builder Implementation
class Director(object):
    def __init__(self, builder):
        self.builder = builder

    # Returns code created.
    def get_code(self):
        self.builder.add_classes()
        return self.builder.get_code()


class AbstractClassBuilder(metaclass=ABCMeta):
    def __init__(self, created_classes):
        self.created_classes = created_classes
        self.all_my_converted_classes = []
        self.all_my_classes = []

    @abstractmethod
    def get_code(self): pass

    @abstractmethod
    def add_classes(self): pass
