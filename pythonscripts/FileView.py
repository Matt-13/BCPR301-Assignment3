# Made by Matt - does console output related statements.
# Code passes the PEP8 Check. 4/04/19
import os


class FileView:
    # File Handler and FileController Methods
    def __init__(self):
        self.error_message = "\n==========ERROR==========\n"
        self.equals = "===================="
        self.minus = "-------------------------------" \
                     "--------------------------------"
        self.directories = {
            "r": self.file_not_found,
            "a": self.file_not_found,
            "lf": self.file_not_found_abs,
            "": self.no_filename_entered
        }

    def general_error(self):   # pragma: no cover
        print(self.error_message)

    # File Controller Methods
    # Made by Liam and Matt
    def print_minus(self):
        print(self.minus)

    def print_help(self):
        # Matt's Code
        print("\n\n")
        print(self.equals +
              " Graph Interpreter Help File " +
              self.equals)
        print("")
        print("NOTE: FileExecuter.py "
              "does not need a command to run")
        print("NOTE: FileExecuter.py "
              "expects a graph.txt in the root directory.")
        print("      if running without a command.")
        print("Command syntax: FileExecuter.py {optionalcommand}")
        print("")
        print("ALLHELP......................."
              "...........................Displays this help page")
        print("LOAD {filename.txt}......................"
              "...Loads a file from the root directory")
        print("ABSLOAD {path_to_file\\filename.txt}......"
              ".....Loads a file from an absolute path")

        # Liam's Code
        print("LOADCODE {Code_ID}......................."
              "..........Loads code from the data base")
        print("PRINTCODE {Code_ID}................."
              "...Prints code from the data base to the cmd")
        print("SAVE {filename.txt}{Code_ID}..........."
              "..Saves code from database to a text file")
        print("PRINTFILE ................................."
              "...........Prints code from self.data")

    @staticmethod
    def fc_defaults(file_location):   # pragma: no cover
        print("Command not entered. Looking for a "
              "Graph.txt in root directory, "
              "and directory above... ")
        print("Looking in: {} {}"
              .format(os.path.abspath(file_location),
                      "and directory above."))

    @staticmethod
    def fc_file_found():   # pragma: no cover
        print("\nFile Found! Reading..\n")

    # Shortened to 1 line with a dict.
    def fc_file_not_found(self, file_location, directory, command):
        self.directories[directory](file_location, command)

    @staticmethod
    def file_not_found(file_location, command):
        print("File not found! There must be a "
              "{}.txt in the chosen directory!"
              .format(file_location))

    @staticmethod
    def no_filename_entered(file_location, command):
        if command == "load":
            print("No filename entered.\n"
                  "Expected Syntax: load {filename.txt}")
        elif command == "absload":
            print("No filename entered.\n"
                  "Expected Syntax: "
                  "absload {path_to_file\\filename.txt}")

    @staticmethod
    def file_not_found_abs(file_location, command):
        print("File not found! '{}'"
              .format(os.path.abspath(file_location)))

    @staticmethod
    def fc_syntax_error(command):
        if command == "load":
            print("Syntax Error\n"
                  "Expected Syntax: load {filename.txt}")
        elif command == "absload":
            print("File Type Error - File must end in .txt!\n"
                  "Expected Syntax: absload "
                  "{path_to_file\\filename.txt}")

    @staticmethod
    def fc_permission_error():   # pragma: no cover
        print("File permission error! "
              "Make sure you have the "
              "correct read permission on the file")

    # File Handler Methods
    # File Converter Methods

    @staticmethod
    def fc_plantuml_converting():   # pragma: no cover
        print("Converting file to python syntax..")

    # File Reader Methods
    @staticmethod
    def fr_plantuml_classes_not_found():   # pragma: no cover
        print("Classes not found! Exiting..")

    @staticmethod
    def fr_file_accepted():   # pragma: no cover
        print("File Accepted.. Continuing..")

    @staticmethod
    def file_written(file):   # pragma: no cover
        print("\nFile(s) Successfully Written to Disk: " +
              file)

    @staticmethod
    def fr_plantuml_error():   # pragma: no cover
        print("File not in PlantUML Syntax! "
              "Program Stopping..")

    # File Executer Methods
    @staticmethod
    def fe_defaults():   # pragma: no cover
        print("\nNo arguments entered.. "
              "Continuing with defaults.")

    @staticmethod
    def fe_too_many_args():   # pragma: no cover
        print("\nToo many arguments entered. "
              "Please enter at most 2.")

    @staticmethod
    def fe_command_syntax(name):   # pragma: no cover
        print("{} requires a filename to {} with\n"
              "Syntax: {} [filename.txt]"
              .format(name, str(name).lower(), name))

    @staticmethod
    def fe_save_id():   # pragma: no cover
        print("Save requires an ID from the database "
              "to save with.\n"
              "Syntax: Save [filename.txt] [ID]")

    @staticmethod
    def fe_loadcode_syntax(text):   # pragma: no cover
        print("{} requires the ID to know which code\n"
              "to load within the database.\n"
              "Syntax: {} [code_id]"
              .format(text, text))

    @staticmethod
    def fe_abs_syntax():   # pragma: no cover
        print("absload requires a file to load.\n"
              "Syntax: absload {path_to_file\\filename.txt}")

    @staticmethod
    def fe_abs_path_error():   # pragma: no cover
        print("Path must be an absolute path.")

    # Other Methods
    # Removed display graph code, display
    # and file error methods as they are all duplication
    @staticmethod
    def output(message):
        print(str(message))

    # FileExecuter CMD Methods
    def next_command(self):
        print(self.minus)
        print("Awaiting next command.. Type "
              "'help' for all available commands.")
        print("To quit the program.. Type "
              "'exit' or 'quit'.")

    @staticmethod
    def test():
        import doctest
        doctest.testfile("../doctests/fileview_doctest.txt", verbose=1)
