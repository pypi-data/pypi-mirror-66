from . import utils


class Student:
    def __init__(self, name="John", surname="Doe"):
        self.mean = None
        self.name = name
        self.surname = surname

    def __lt__(self, other):
        return self.mean < other.mean

    def set_name(self, name):
        self.name = name

    def set_surname(self, surname):
        self.surname = surname

    def set_scores(self, scores):
        self.mean = utils.mean(scores)
        self.scores = scores
     
