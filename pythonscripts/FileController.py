# Code passes the PEP8 check. 4/04/19

# Ignore errors here.
from pythonscripts.FileHandler import FileConverter
from pythonscripts.FileView import FileView
from pythonscripts.FileWriter import FileWriter
import os
from pythonscripts.DataBase import DataBase

fconv = FileConverter()
fw = FileWriter()
fv = FileView()
db = DataBase()


# Some work on observers.
class Observer:
    observers = []

    def __init__(self):
        self.observers.append(self)
        self.observables = {}

    def observe(self, event_name, callback):
        self.observables[event_name] = callback


# Event for fail converting file
class EventFailConvert:
    def __init__(self, name, data, auto_fire=True):
        self.name = name
        self.data = data
        if auto_fire:
            self.fire()

    def fire(self):
        for observer in Observer.observers:
            if self.name in observer.observables:
                observer.observables[self.name](self.data)


# Event for finish converting file
class EventFinishConvert:
    def __init__(self, name, data, auto_fire=True):
        self.name = name
        self.data = data
        if auto_fire:
            self.fire()

    def fire(self):
        for observer in Observer.observers:
            if self.name in observer.observables:
                observer.observables[self.name](self.data)


class FileController(Observer):
    def __init__(self):
        Observer.__init__(self)
        self.data = 'empty'
        self.loop_running = False
        self.get_commands = {
            "": self.no_command,
            "load": self.load_command,
            "absload": self.absload_command
        }

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
            fconv.convert_file()
            fconv.return_program()
            self.write_file()
        except IOError:  # pragma: no cover
            print("System failed to save to file")
        except Exception as e:  # pragma: no cover
            fv.general_error()
            print("An error has occurred" + str(e))

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
