from abc import ABCMeta, abstractmethod


class PartDirector(object):
    def __init__(self, builder):
        self.builder = builder

    def direct(self, *args):
        self.builder.set_args(self.builder, *args)
        return self.builder.__str__(self.builder)


class ClassParts:
    def __init__(self):
        self.all_my_parts = []

    def set_attribute(self, parts):
        self.all_my_parts.append(parts)

    def return_self(self):
        return self.all_my_parts


class AbstractPartBuilder(metaclass=ABCMeta):
    def __init__(self, *args):
        self.my_name = None
        self.my_return = None
        self.my_type = None

    @abstractmethod
    def set_args(self, *args): pass

    @abstractmethod
    def __str__(self): pass


class AttributeBuilder(AbstractPartBuilder):
    def set_args(self, new_name, new_return):
        self.my_name = new_name
        self.my_return = new_return

    def __str__(self):
        self.my_name = self.my_name.strip(' ')
        self.returns = {
            "String": f"    {self.my_name}: str",
            "Integer": f"    {self.my_name}: int",
            "ArrayObject": f"    {self.my_name}: list",
            "Object": f"    {self.my_name}: object"
        }
        return self.returns[self.my_return]


class MethodBuilder(AbstractPartBuilder):
    def set_args(self, new_name, new_return):
        self.my_name = new_name.replace("()", "")
        self.my_return = new_return

    def __str__(self):
        return f"    def {self.my_name}(self):\n        pass"


class RelationshipBuilder(AbstractPartBuilder):
    def set_args(self, new_type):
        self.my_name = new_type[1]
        self.my_type = new_type[0]

    def __str__(self):
        return f"{self.my_name}s"
