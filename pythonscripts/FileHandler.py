""" Made by 3 students:
    Matthew Whitaker
    Liam Brydon
    Sarah Ball (providing the model)
"""
# Code passes the PEP8 Check. 4/04/19

import datetime
import re
# from abc import abstractmethod, ABCMeta
from pythonscripts.ClassPartsBuilder import PartDirector, \
    AttributeBuilder, MethodBuilder, RelationshipBuilder, \
    ClassPart
from pythonscripts.FileView import FileView
fv = FileView()


class FileConverter:
    def __init__(self):
        self.class_info = ""
        self.classes = []
        self.data = ""
        self.converted_classes = []
        self.my_relationship_content = ""
        self.codeToText = ""
        self.class_name = ""
        self.attributes = []
        self.methods = []
        self.relationships = []

    # Made by Sarah - Modified by Matt
    def convert_file(self):
        fv.fc_plantuml_converting()
        for self.class_info in self.classes:
            self.attributes = []
            self.methods = []
            self.relationships = []
            self.class_name = self.class_info.split(' ')[1]
            self.convert_attributes()
            self.convert_methods()
            self.convert_relationships()
            self.add_class(self.class_name, self.attributes, self.methods, self.relationships)

    def convert_attributes(self):
        for line in self.class_info.split("\n"):
            if line.find(":") != -1:
                self.attributes.append(line)

    def convert_methods(self):
        for line in self.class_info.split("\n"):
            if line.find("()") != -1:
                self.methods.append(line)

    def convert_relationships(self):
        for relationship in self.my_relationship_content.split("\n"):
            if self.find_relationship(relationship, self.class_name):
                self.relationships.append(
                    self.find_relationship(relationship, self.class_name))

    # Made by Sarah
    def add_class(self, class_name, attributes, methods, relationships):   # pragma: no cover
        new_class = ClassBuilder(class_name, attributes,
                                 methods, relationships)
        new_class.add_class_attributes()
        new_class.add_class_methods()
        self.converted_classes.append(new_class)

    # Some work on relationships
    def find_relationship(self, relationship, class_name):   # pragma: no cover
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

    def return_program(self):   # pragma: no cover
        out = "# File generated & created on: " + str(datetime.datetime.now())
        out += "\n# File passes the PEP8 check."
        out += "\n\n"
        for x in self.converted_classes:
            out += (x.return_class())
        # out += ""
        self.codeToText += out

    def read_file(self, file):   # pragma: no cover
        with open(file, "r") as filename:
            self.data = filename.read()
        read_uml = FileReader(self.data)
        self.classes = read_uml.find_classes()
        self.my_relationship_content = \
            self.classes[len(self.classes) - 1]

    @staticmethod
    def test():   # pragma: no cover
        import doctest
        doctest.testfile("../doctests/filehandler_doctest.txt", verbose=1)


fc = FileConverter()


# Made by Liam & Matt
class FileReader:
    def __init__(self, filename):
        self.allMyClasses = []
        self.code = filename

    # Made by Matt
    def check_if_plantuml(self, code):   # pragma: no cover
        is_plantuml = False
        try:
            if code.startswith("@startuml") and code.endswith("@enduml"):
                is_plantuml = True
        except IOError:
            fv.general_error()
            print("The file cannot be read.")
        except EOFError:
            fv.general_error()
            print("Unexpected End of File.")
        except TypeError:
            fv.general_error()
            print("The file must contain a string.")
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))
        return is_plantuml

    # Made by Liam
    # Check if the file contains the word "Class"
    def count_occurrences(self, word, sentence):   # pragma: no cover
        try:
            lower = sentence.lower()
            split = lower.split()
            count = split.count(word)
            if count == 0:
                fv.fr_plantuml_classes_not_found()
            return count
        except TypeError:
            fv.general_error()
            print("The file must contain a string.")
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))

    def find_classes(self):   # pragma: no cover
        try:
            is_plantuml = self.check_if_plantuml(self.code)
            if is_plantuml:
                fv.fr_file_accepted()
                value = self.count_occurrences("class", self.code)
                for i in range(0, value):
                    self.allMyClasses.append(self.code.split("}\nclass")[i])
                return self.allMyClasses
            else:
                fv.fr_plantuml_error()
        except TypeError:
            fv.general_error()
            print("The file must contain a string.")
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))


# Client
class ClassBuilder:
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
        self.PD = PartDirector(None)

    # Client
    def add_class_attributes(self):
        self.PD.set_builder(AttributeBuilder)
        self.all_my_attributes = self.PD.direct(self.attributes)

    # Client
    def add_class_methods(self):
        self.PD.set_builder(MethodBuilder)
        self.all_my_methods = self.PD.direct(self.methods)

    # Client
    def add_class_relationships(self):  # pragma: no cover
        self.PD.set_builder(RelationshipBuilder)
        relationships = []
        for a_relationship in self.all_my_relationships:
            if "comp" in a_relationship:
                relationships.append(a_relationship)
            if "aggreg" in a_relationship:
                relationships.append(a_relationship)
            if "assoc" in a_relationship:
                relationships.append(a_relationship)
        self.all_my_relationships = self.PD.direct(relationships)

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
