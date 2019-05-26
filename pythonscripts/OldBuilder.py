from abc import ABCMeta, abstractmethod


# Director
class PartDirector(object):
    def __init__(self, builder):
        self.builder = builder
        self.CP = ClassPart()

    def set_builder(self, builder):
        self.builder = builder

    def direct(self, *args):
        self.builder.set_args(self.builder, *args)
        self.CP.set_parts(self.builder.__str__(self.builder))
        return self.CP.get_parts()


# Product
class ClassPart:
    def __init__(self):
        self.all_my_parts = list()

    def set_parts(self, parts):
        self.all_my_parts = parts

    def get_parts(self):
        return self.all_my_parts


# Abstract Builder
class AbstractPartBuilder(metaclass=ABCMeta):
    def __init__(self):
        self.methods = None
        self.attributes = None
        self.my_name = None
        self.my_return = None
        self.my_type = None

    @abstractmethod
    def set_args(self, *args): pass

    @abstractmethod
    def __str__(self): pass


# Builder: Attributes
class AttributeBuilder(AbstractPartBuilder):
    def set_args(self, attribs):
        self.attributes = attribs

    def __str__(self):
        all_my_attributes = []
        for an_attribute in self.attributes:
            self.my_name = an_attribute.split(": ")[0]
            self.my_return = an_attribute.split(": ")[1]
            self.my_name = self.my_name.strip(' ')
            returns = {
                "String": f"    {self.my_name}: str",
                "Integer": f"    {self.my_name}: int",
                "ArrayObject": f"    {self.my_name}: list",
                "Object": f"    {self.my_name}: object"
            }
            all_my_attributes.append(returns[self.my_return])
        return all_my_attributes


# Builder: Methods
class MethodBuilder(AbstractPartBuilder):
    def set_args(self, methods):
        self.methods = methods

    def __str__(self):
        all_my_methods = []
        for a_method in self.methods:
            new_m_name = a_method.split(":")[0]
            new_m_return = a_method.split("()")[1]
            self.my_name = new_m_name.replace("()", "")
            self.my_return = new_m_return
            all_my_methods.append("    def " + self.my_name
                                  + "(self):\n"
                                    "        "
                                    "pass")
        return all_my_methods


# Builder: Relationships
class RelationshipBuilder(AbstractPartBuilder):
    def set_args(self, new_type):
        self.my_name = new_type[1]
        self.my_type = new_type[0]

    def __str__(self):
        return f"{self.my_name}s"
