# Code passes the PEP8 check. 4/04/19

# Ignore errors here.
from pythonscripts.FileHandler import FileConverter
from pythonscripts.FileView import FileView
from pythonscripts.FileWriter import FileWriter
import os
import abc
from pythonscripts.DataBase import DataBase

fconv = FileConverter()
fw = FileWriter()
fv = FileView()
db = DataBase()


# Some work on observers.
class Observer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._subject = None
        self._state = None

    @abc.abstractmethod
    def update(self, arg):
        pass


# Read Event handler
class ObserverEvent(Observer):
    def update(self, arg):
        self._state = arg
        fconv.convert_file()
        fconv.return_program()
        print(self._state)


# Line Printer
class ObserverPrinter(Observer):
    def update(self, arg):
        self._state = arg
        print("--------------------------------"
              "-------------------------------")


OE = ObserverEvent()
OP = ObserverPrinter()


class FileController:
    def __init__(self):
        self._observers = set()
        self._state = None
        self.data = 'empty'
        self.loop_running = False
        self.get_commands = {
            "": self.no_command,
            "load": self.load_command,
            "absload": self.absload_command
        }
        self.attach(OP)
        self.attach(OE)

    # Observer Implementation
    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def _notify(self):
        print("Checking for Errors...")
        for observer in self._observers:
            observer.update(self._state)

    @property
    def subject_state(self):
        return self._state

    # Old Code
    def user_choose(self):   # pragma: no cover
        self.loop_running = True  # doctest: +SKIP
        while self.loop_running:
            userinput = input("Would you like to view the file"
                              "in your default text editor? (Y/N) ")
            if userinput.lower() == "y":
                os.startfile("Output.txt")
                break
            elif userinput.lower() == "n":
                break
            else:
                print("Please enter either Y or N.. "
                      "{} was entered.".format(userinput))
                pass
        self.loop_running = False

    def handle_command(self, cmd, file_location):
        try:
            self.get_commands[cmd](file_location)
        except FileNotFoundError:  # pragma: no cover
            fv.fc_file_not_found(file_location, "lf", "")

    @staticmethod
    def is_file(filename):
        if os.path.isfile("{}".format(filename)):
            return True
        elif os.path.isfile("./{}".format(filename)):  # pragma: no cover
            return True
        else:
            return False

    def no_command(self, file_location):
        fv.fc_defaults(file_location)
        try:
            if self.is_file("Graph.txt"):
                fv.fc_file_found()
                self.read_file("./Graph.txt")
                # self.user_choose()
            else:
                fv.output("Graph.txt Not Found in root!")  # pragma: no cover
        except FileNotFoundError:  # pragma: no cover
            fv.general_error()
            fv.fc_file_not_found(file_location, "r", "")

    def load_command(self, file_location):
        if file_location.endswith(".txt"):
            try:
                if self.is_file(file_location):
                    fv.fc_file_found()
                    self.read_file("./{}".format(file_location))
                    # self.user_choose()
                else:
                    fv.output("File Not Found! '{}'".format(file_location))
            except FileNotFoundError:  # pragma: no cover
                fv.general_error()
                fv.fc_file_not_found(file_location, "r", "load")
            except PermissionError:  # pragma: no cover
                fv.general_error()
                fv.fc_permission_error()
        else:
            self.command_error(file_location, "load")

    # Will look at refactoring when I start with Long Methods.
    def absload_command(self, file_location):
        if file_location.endswith(".txt"):
            try:
                if self.is_file(file_location):
                    fv.fc_file_found()
                    self.read_file("{}".format(file_location))
                    # self.user_choose()
                else:
                    fv.general_error()
                    fv.fc_file_not_found(file_location, "lf", "")
            except FileNotFoundError:  # pragma: no cover
                fv.fc_file_not_found(file_location, "a", "absload")
            except PermissionError:  # pragma: no cover
                fv.fc_permission_error()
        else:
            self.command_error(file_location, "absload")

    @staticmethod
    def command_error(file_location, cmd):
        fv.general_error()
        if file_location == "":
            fv.fc_file_not_found(file_location, "", cmd)
        else:
            fv.fc_syntax_error("absload")

    def read_file(self, filename):
        try:
            fconv.read_file(filename)
            self._state = "Done!"
            self._notify()
            self.write_file()
        except IOError:  # pragma: no cover
            self._state = "Error: System Failed to Save to File!"
            self._notify()
        except Exception as e:  # pragma: no cover
            self._state = "An error has occurred" + str(e)
            self._notify()
            fv.general_error()

    def write_file(self):
        self.data = fconv.codeToText
        db.data_entry(self.data)
        fw.write_file(self.data, "Output.txt")

    # Liam
    def save_file(self, file_name, code_id):
        self.data = db.get_code(code_id)
        try:
            fw.write_file(db.get_code(code_id), file_name)
        except IOError as e:  # pragma: no cover
            print("System failed to save to file" + e)
        except Exception as e:  # pragma: no cover
            fv.general_error()
            print("An error has occurred" + str(e))

    # Liam
    def load_code(self, code_id):
        try:
            code = db.get_code(code_id)
            if code != '':
                self.data = code
                fv.output("Code has loaded successfully")
            else:
                fv.output("ERROR: code failed to load:" + '\t' + code)  # pragma: no cover
        except IOError:  # pragma: no cover
            print("System failed to save to file")
        except Exception as e:  # pragma: no cover
            fv.general_error()
            print("An error has occurred" + str(e))

    # Liam
    def print_code(self, code_id):  # pragma: no cover
        try:
            code = db.get_code(code_id)
            if code != '':
                fv.output(code)
            else:
                fv.output("ERROR: code failed to load:")
                fv.output('\t' + code)
        except ValueError and TypeError:  # pragma: no cover
            fv.output("Please enter an integer")
        except IOError as e:  # pragma: no cover
            print("System failed to load to file" + e)

    # Matthew - Possible Middle Man Smell..
    @staticmethod
    def view_help():  # pragma: no cover
        fv.print_help()

    @staticmethod
    def test():  # pragma: no cover
        import doctest
        doctest.testfile("../doctests/filecontroller_doctest.txt", verbose=1)
