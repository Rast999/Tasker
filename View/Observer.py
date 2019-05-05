"""
    Observer pattern
"""


class Observable:

    def __init__(self):
        self.observers = []

    def add(self, *args):
        for obs in args:
            self.observers.append(obs)

    def remove(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for obs in self.observers:
            obs.update()


class Observer:

    def update(self):
        raise NotImplementedError("This method should be overwritten in the children")