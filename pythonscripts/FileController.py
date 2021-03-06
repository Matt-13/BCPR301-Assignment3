# Code passes the PEP8 check. 4/04/19
import os
from pythonscripts.FileHandler import FileConverter
from pythonscripts.FileView import FileView
from pythonscripts.FileWriter import FileWriter
from pythonscripts.DataBase import DataBase
from pythonscripts.Observer import ObserverRead, ObserverWrite, \
    ObserverCheck, Subject

fconv = FileConverter()
fw = FileWriter()
fv = FileView()
db = DataBase()
OR = ObserverRead()
OW = ObserverWrite()
OC = ObserverCheck()


# Concrete Subject
class FileController(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.data = 'empty'
        self.loop_running = False
        self.get_commands = {
            "": self.no_command,
            "load": self.load_command,
            "absload": self.absload_command
        }
        self.attach(OW)
        self.attach(OR)
        self.attach(OC)

    # Observer Implementation
    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)
        print("Attached an observer: " + observer.__class__.__name__)

    def detach(self, observer):
        self._observers.remove(observer)
        print("Detached an observer: " + observer.__class__.__name__)

    def notify(self):
        for observer in self._observers:
            observer.update()

    def set_state(self, state):
        self._state = state

    def get_state(self):
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
        self.set_state(None)
        try:
            self.data = fconv.read_file(filename)
            self.set_state(1)
            # Notify the observers that the program has finished
            # reading and converting the file.
            self.notify()
            self.write_file()
        except IOError:  # pragma: no cover
            self.set_state("Error: System Failed to Save to File!")
            self.notify()

    def write_file(self):
        fv.print_minus()
        print("Writing File...")
        fw.write_file(self.data, "Output.txt")
        print("Done!")
        fv.print_minus()
        self.code_to_db()

    def code_to_db(self):
        db.data_entry(self.data)

    # Liam
    def save_file(self, file_name, code_id):
        self.data = db.get_code(code_id)
        try:
            fw.write_file(db.get_code(code_id), file_name)
        except IOError as e:  # pragma: no cover
            self.set_state("System failed to save to file" + e)
            self.notify()

    # Liam
    def load_code(self, code_id):
        try:
            code = db.get_code(code_id)
            if code != '':
                self.data = code
                fv.output("Code has loaded successfully")
            else:
                self.set_state("ERROR: code failed to load:" + '\t' + code)
                self.notify()
        except IOError:  # pragma: no cover
            self.set_state("System failed to save to file")
            self.notify()

    # Liam
    def print_code(self, code_id):  # pragma: no cover
        try:
            code = db.get_code(code_id)
            if code != '':
                fv.output(code)
            else:
                self.set_state("ERROR: code failed to load:")
                self.notify()
        except ValueError and TypeError:  # pragma: no cover
            self.set_state("Please enter an integer")
            self.notify()
        except IOError as e:  # pragma: no cover
            self.set_state("System failed to load to file" + e)
            self.notify()

    # Matthew - Possible Middle Man Smell..
    @staticmethod
    def view_help():  # pragma: no cover
        fv.print_help()

    @staticmethod
    def test():  # pragma: no cover
        import doctest
        doctest.testfile("../doctests/filecontroller_doctest.txt", verbose=1)
