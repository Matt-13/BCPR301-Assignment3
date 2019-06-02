from pythonscripts.FileView import FileView
from abc import ABCMeta, abstractmethod

fv = FileView()


# Some work on observers.
class Observer(metaclass=ABCMeta):
    def __init__(self):
        self._subject = None
        self._state = None

    @abstractmethod
    def update(self):
        pass


# Read Event handler - Concrete Observer
# Good Day Scenario
class ObserverRead(Observer):
    def update(self):
        self._state = self._subject.get_state()
        if self._state == 1:
            print("Error Checking Complete.")
            print("No Errors Found!")


# Write File Wrapper Observer - Concrete Observer
class ObserverWrite(Observer):
    def update(self):
        self._state = self._subject.get_state()
        if self._state == 1:
            fv.print_minus()


# Observes Errors. - Concrete Observer
# Bad Day Scenario
class ObserverCheck(Observer):
    def update(self):
        self._state = self._subject.get_state()
        if self._state != 1:
            fv.general_error()
            fv.output(self._state)


class Subject(metaclass=ABCMeta):
    def __init__(self):
        self._state = 0
        self._observers = set()

    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass
