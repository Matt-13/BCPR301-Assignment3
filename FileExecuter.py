# Ignore errors below this line.
import sys
import os
import cmd
import coverage
import doctest
from pythonscripts.FileController import FileController
from pythonscripts.FileView import FileView

# Execute code here
# Matthew Whitaker's code.
fv = FileView()
fc = FileController()


# 4/04/19 Code passes the PEP8 Check.
# CMD based code - Matt

# Could do a mediator design pattern between the command classes
# or implement the command design pattern between them as well.

class Main(cmd.Cmd):
    def __init__(self):
        super(Main, self).__init__()
        self.intro = \
            "===============================================\n" \
            "PlantUML to Python Converter\n" \
            "Please type 'help' for all available commands.\n" \
            "Please type 'allhelp' to view the help file.\n" \
            "To continue with a default graph.txt in the\n" \
            "root directory, press [Enter]\n" \
            "=============================================="
        self.interrupt = "Ctrl + C pressed, but ignored. " \
                         "Please use 'exit' or 'quit' " \
                         "to stop the program."
        self.verifycommand = "Please verify your command, and try again."
        self.error = "An error has occurred."

    # CMD - Matt
    # Cannot test a loop so will not be covered using doctests.
    def cmdloop(self, intro=None):  # pragma: no cover
        # self.do_tests()  # first instance of duplication
        print(self.intro)
        while True:
            try:
                super(Main, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print(self.interrupt)
            except TypeError and ValueError:
                fv.general_error()
                print(self.verifycommand)
            except Exception:
                fv.general_error()
                print(self.error)

    # Continues when no command is entered - Matt
    def emptyline(self):
        fv.fe_defaults()
        fc.handle_command('', '')
        fv.next_command()

    # Load method - Matt
    def do_load(self, line):
        """
        LOADS your SOURCE PlantUML text file, and translates it
        into a python file, from the current working directory.
        Usage: LOAD [filename.txt]
        """
        fc.handle_command("load", line)
        fc.observe("File Loaded Successfully", fc.read_file)
        fv.next_command()

    # Absload method - Matt
    def do_absload(self, line):
        """
        LOADS your SOURCE PlantUML text file, and translates it
        into a python file, from the directory of your choosing.
        Usage: ABSLOAD [path_to_filename.txt]
        """
        if "\\" in line:
            fc.handle_command("absload", line)
            fc.observe("File Loaded Successfully", fc.read_file)
        else:
            fv.general_error()
            fv.fe_abs_path_error()
        # Next instance of duplication removed.
        fv.next_command()

    # View help file - Matt and Liam
    def do_allhelp(self, line):
        """
        SHOWS all HELP relating to this program.
        Usage: ALLHELP
        """
        fv.print_help()
        fv.next_command()

    # Exit method - Matt
    def do_exit(self, line):  # pragma: no cover
        # + can't be tested as it will stop the program.
        """
        STOPS and EXITS the program.
        YOUR DATA WILL NOT BE SAVED.
        Usage: quit, exit, q, stop
        """
        exit()

    # Instances of duplication removed by assigning do_quit and do_q to do_exit
    do_quit = do_q = do_stop = do_exit

    # Save method - Liam
    def do_save(self, line):
        """
        Saves the converted plantuml code from the database to a textfile
        Usage: save {filename.txt} {code_id}
        """
        line = line.split(' ')
        fc.save_file(line[0], line[1])
        fv.next_command()

    # Printcode method - Liam
    def do_printcode(self, line):
        """
        Prints the converted plantuml code from the database to the cmd
        Usage: printcode {code_id}
        """
        fc.print_code(line)
        fv.next_command()

    # Loadcode method - Liam
    def do_loadcode(self, line):
        """
        Loads code from the database into self.data
        Usage: loadcode {code_id}
        """
        fc.load_code(line)
        fv.next_command()

    # Printfile method - Liam
    def do_printfile(self, line):
        """
        Prints the data saved inside self.data to the cmd
        Usage: printfile
        """
        fc.print_file()
        fv.next_command()  # pragma: no cover

    @staticmethod
    def test():
        import doctest
        doctest.testfile("./doctests/fileexecuter_main_doctest.txt", verbose=1)


m = Main()


class SystemArgs:
    def __init__(self):
        self.command = ""
        self.commandargs = ""
        self.command_dictionary = {
            "absload": self.do_absload_command, "load": self.do_load_command,
            "loadcode": self.do_load_command, "help": self.do_help_command,
            "save": self.do_save_command,
            "printcode": self.do_printcode_command
        }
        self.args = sys.argv[1:]

    def check_if_commands_present(self):
        # If there is commands then:
        if len(self.args) > 3:
            fv.general_error()
            fv.fe_too_many_args()
        elif len(self.args) >= 1:
            self.command = str(sys.argv[1]).lower()
            self.check_command = self.check_command()
        # Otherwise, Start the CMD.cmdloop
        else:
            m.cmdloop()  # pragma: no cover

    def check_if_commandargs_present(self):
        if len(self.args) == 2:
            return True
        else:
            fv.output("Too many arguments entered.")
            return False

    def check_if_saveargs_present(self):
        if len(self.args) == 3:
            return True
        else:
            return False

    def check_command(self):
        if self.command in self.command_dictionary:
            fv.output("Command Found.. Parsing..")
            self.command_to_function()
        else:
            fv.output("'" + self.command + "' Command not Found, "
                                           "type 'FileExecuter.py help' "
                                           "for all available commands.")

    def command_to_function(self):
        # Successful removal of a large block of if/else statements.
        self.command_dictionary[self.command]()

    @staticmethod
    def do_help_command():
        fc.view_help()

    def do_absload_command(self):
        if self.check_if_commandargs_present():
            if "\\" in str(sys.argv[2]):
                fc.handle_command("absload", str(sys.argv[2]))
                fc.observe("File Loaded Successfully", fc.read_file)
            else:
                fv.general_error()
                fv.fe_abs_path_error()
        else:
            fv.general_error()
            fv.fe_abs_syntax()

    def do_load_command(self):
        if self.check_if_commandargs_present():
            # User_choose seems to break the code
            # when this is run from testing
            # User_choose has been disabled for tests to run.
            fc.handle_command("load", str(sys.argv[2]))
            fc.observe("File Loaded Successfully", fc.read_file)
        else:
            fv.general_error()
            fv.fe_command_syntax("Load")

    def do_save_command(self):
        if self.check_if_saveargs_present():
            # Old if statement doesn't even get reached.
            fc.save_file(sys.argv[2], sys.argv[3])
        else:
            fv.general_error()
            fv.fe_command_syntax("Save")

    def do_loadcode_command(self):
        if self.check_if_commandargs_present():
            fc.load_code(sys.argv[2])
        else:
            fv.general_error()
            fv.fe_loadcode_syntax("loadcode")

    def do_printcode_command(self):
        if self.check_if_commandargs_present():
            fc.print_code(sys.argv[2])
        else:
            fv.general_error()
            fv.fe_loadcode_syntax("printcode")

    @staticmethod
    def test():
        import doctest
        doctest.testfile("./doctests/fileexecuter_sysargs_doctest.txt",
                         verbose=1)


if __name__ == "__main__":  # pragma: no cover
    # To run tests, run Tests.py
    a = SystemArgs()
    a.check_if_commands_present()
