from pythonscripts.FileController import FileController
from pythonscripts.FileView import FileView
from FileExecuter import Main
from FileExecuter import SystemArgs


class Tests:
    def __init__(self):
        self.fv = FileView()
        self.fc = FileController()
        self.main = Main()
        self.sys_args = SystemArgs()

    def do_tests(self):
        self.fc.test()  # Test FileController and FileHandler
        self.fv.test()  # Test FileView
        self.main.test()  # Test FileExecuter Main
        self.sys_args.test()  # Test FileExecuter SysArgs


if __name__ == "__main__":
    T = Tests()
    T.do_tests()
