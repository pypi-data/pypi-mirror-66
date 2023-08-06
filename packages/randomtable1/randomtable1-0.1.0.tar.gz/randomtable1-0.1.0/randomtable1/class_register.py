from faker import Faker
from prettytable import PrettyTable

class ClassRegister:
    def __init__(self, name=None, teacher=None):
        self.name = name
        self.students = []
        self.teacher = teacher

    def __len__(self):
        len_stud = len(self.students)
        if self.teacher is not None:
            len_stud += 1
        return len_stud

    def __getitem__(self, key):
        if self.teacher is not None:
            if key == 0:
                return self.teacher
            else:
                return self.students[key-1]
        else:
            return self.students[key]


    def add_random_student(self):
        fake_name = Faker()
        for i in range(10):
            self.students.append(fake_name.name())

    def add_students(self, *students):
        self.students += students

    def sort_students_by_mean(self):
        self.students.sort()

    def compare_students(self, student_a, student_b):
        return student_a.mean < student_b.mean

    def print_student(self):
        for student in self.students:
            print(student.name, student.scores)

    def set_scores(self, **students):
        for name, scores in students.items():
            for student in self.students:
                if student.name == name:
                    student.set_scores(scores)

    def create_table(self):
        table = PrettyTable()
        table.add_column("Students_names", self.students)
        return table

