# Code passes the PEP8 Check. 26/05/19

import re
import datetime
from pythonscripts.FileView import FileView
from pythonscripts.NewBuilder import AbstractClassBuilder, Director
fv = FileView()


class CodeBuilder(AbstractClassBuilder):
    def add_classes(self):
        fv.fc_plantuml_converting()

        for a_class in self.created_classes:
            new_c_class = Translator(a_class)
            new_c_class.make_class()

            new_class = CreatedClass(new_c_class.class_name,
                                     new_c_class.attributes,
                                     new_c_class.methods,
                                     new_c_class.relationships)

            new_class.add_class_attributes()
            new_class.add_class_methods()
            self.all_my_classes.append(new_class)

    def get_code(self):
        out = '# Code Passes PEP8 Checks.\n'
        out += '# File Generated on: ' \
            f'{datetime.datetime.now()}\n'
        for a_class in self.all_my_classes:
            out += a_class.return_class()
        return out


class FileConverter:
    def __init__(self):
        self.code = ''
        self.uml_classes = []

    def read_file(self, filename):
        with open(filename, "r") as filename:
            data = filename.read()

        read_uml = FileReader(data)
        my_data = read_uml.find_classes()

        self.code = Director(CodeBuilder(my_data)).get_code()
        return self.code

    @staticmethod
    def test():   # pragma: no cover
        import doctest
        doctest.testfile("../doctests/filehandler_doctest.txt", verbose=1)


fc = FileConverter()


class Translator:
    def __init__(self, new_class):
        self.new_class = new_class
        self.class_name = ''
        self.attributes = []
        self.methods = []
        self.relationships = []

    def make_class(self):
        self.class_name = self.new_class.split(' ')[1]
        for line in self.new_class.split("\n"):
            if line.find(":") != -1:
                self.attributes.append(line)

        for line in self.new_class.split("\n"):
            if line.find("()") != -1:
                self.methods.append(line)

        for relationship in self.new_class.split("\n"):
            if self.find_relationship(relationship, self.class_name):
                self.relationships.append(
                    self.find_relationship(relationship, self.class_name))

    # Somehow this got broken. Need to fix.
    @staticmethod
    def find_relationship(relationship, class_name):
        if relationship.startswith(class_name):
            pass
        elif relationship.endswith(class_name):
            if len(relationship.split(" ")) < 2:
                pass
            elif re.search(r"-->", relationship):
                ext_class = relationship.split(" ")[0]
                return tuple(("association of", ext_class))
            elif re.search(r"\*--", relationship):
                com_class = relationship.split(" ")[0]
                return tuple(("composition of", com_class))
            elif re.search(r"o-", relationship):
                as_class = relationship.split(" ")[0]
                return tuple(("aggregation of", as_class))


# Made by Liam & Matt
class FileReader:
    def __init__(self, filename):
        self.allMyClasses = []
        self.code = filename

    @staticmethod
    def check_if_plant_uml(code):   # pragma: no cover
        is_plant_uml = False
        try:
            if code.startswith("@startuml") and code.endswith("@enduml"):
                is_plant_uml = True
        except IOError:
            fv.general_error()
            print("The file cannot be read.")
        return is_plant_uml

    @staticmethod
    def count_occurrences(word, sentence):   # pragma: no cover
        try:
            lower = sentence.lower()
            split = lower.split()
            count = split.count(word)
            if count == 0:
                fv.fr_plantuml_classes_not_found()
            return count
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))

    def find_classes(self):   # pragma: no cover
        try:
            is_plant_uml = self.check_if_plant_uml(self.code)
            if is_plant_uml:
                fv.fr_file_accepted()
                value = self.count_occurrences("class", self.code)
                for i in range(0, value):
                    self.allMyClasses.append(self.code.split("}\nclass")[i])
                return self.allMyClasses
            else:
                fv.fr_plantuml_error()
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))


class CreatedClass:
    def __init__(self, class_name, new_attributes, new_methods, relationships):
        self.name = class_name
        self.attributes = new_attributes
        self.methods = new_methods
        self.relationships = relationships
        self.all_my_attributes = []
        self.all_my_methods = []
        self.all_my_relationships = []
        self.all_my_associated_classes = []
        self.all_my_aggregated_classes = []
        self.all_my_composite_classes = []

    def add_class_attributes(self):
        for an_attribute in self.attributes:
            new_a_name = an_attribute.split(": ")[0]
            new_a_return = an_attribute.split(": ")[1]
            new_a = Attribute(new_a_name, new_a_return)
            self.all_my_attributes.append(new_a)

    def add_class_methods(self):
        for a_method in self.methods:
            new_m_name = a_method.split(":")[0]
            new_m_return = a_method.split("()")[1]
            new_m = Method(new_m_name, new_m_return)
            self.all_my_methods.append(new_m)

    # Some work on relationships
    def add_class_relationships(self):
        for a_relationship in self.all_my_relationships:
            if "comp" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_composite_classes.append(new_relationship)
            if "aggreg" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_aggregated_classes.append(new_relationship)
            if "assoc" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_associated_classes.append(new_relationship)

    # Made by Liam
    def return_class(self):
        out = "" + str("\nclass {}:\n\n").format(self.name)
        out += self.return_class_attributes()
        out += self.return_class_relationships()
        out += self.return_class_methods()
        return out

    def return_class_attributes(self):
        out = ""
        length = len(self.all_my_attributes)
        count = 0
        for x in self.all_my_attributes:
            if count == length - 1:
                out += str("{}".format(x)) + str("\n\n")
                count += 1
            elif count < length:
                out += str("{}".format(x)) + str("\n")
                count += 1
        return out

    def return_class_relationships(self):
        out = ""
        out += str("    " + "def __init__(self):\n")
        for a_class in self.relationships:
            out += str(
                "        "
                f"self.{str(a_class[1]).lower()}"
                f" = {a_class[1]}()  "
                f"# {a_class[0]}\n"
            )
        out += "\n" + str("        " + "pass\n\n")
        return out

    def return_class_methods(self):
        out = ""
        for x in self.all_my_methods:
            out += str("{}".format(x))
            out += str("\n\n")
        return out


class Attribute:
    def __init__(self, new_name, new_return):
        self.name = new_name
        self._return = new_return
        self.name = self.name.strip(' ')

        self.output = {
            "String": f"    {self.name}: str",
            "Integer": f"    {self.name}: int",
            "ArrayObject": f"    {self.name}: list",
            "Object": f"    {self.name}: object"
        }

    def __str__(self):
        return self.output[self._return]


class Method:
    def __init__(self, new_name, new_return):
        self.name = new_name.replace("()", "")
        self._return = new_return

    def __str__(self):
        return f"    def {self.name}(self):\n        pass"


class Relationship:
    def __init__(self, new_type):
        self.name = new_type[1]
        self.type = new_type[0]

    def __str__(self):
        return f"{self.name}s"
