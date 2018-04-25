
# coding: utf-8

class instructorObj():
    def __init__(self, name):
        self.name = name
        self.classes = []
        self.departments = []
        self.office = ''
        self.phone = ''
        self.email = ''
        self.year = ''
        self.quarter = ''

    def __str__(self):
        return self.name

    def print_schedule(self):
        print(self.name)
        print()
        for x in self.classes:
            print(x.course_number)
            print(x.course_name)
            print(x.day)
            print(x.start_time)
            print(x.end_time)
            print(x.building)
            print(x.room_number)
            print()

