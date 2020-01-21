# objects.py

"""
module for the objects in the schedule app


"""


class TimeBlock:
    def __init__(
        self,
        id=None,
        CRN=None,
        building=None,
        course_num=None,
        course_title=None,
        day=None,
        department=None,
        location=None
        instructor=None,
        is_class=True,
        is_office_hours=False,
        quarter=None,
        year=None,
    ):
        self.id = id  # int
        self.start_time = start_time  # datetime
        self.end_time = end_time  # datetime
        self.day = day  # str
        self.CNR = CRN  # int
        self.room = room  # Room class object
        self.course_code = course_code  # str
        self.course_name = course_name  # str
        self.instructor = instructor  # Instructor class object
        self.is_class = is_class  # bool
        self.is_office_hours = is_office_hours  # bool
        self.quarter = quarter  # str
        self.year = year  # int

    def __str__(self):
        if (
            self.day
            and self.start_time
            and self.end_time
            and self.course_code
            and self.room
        ):
            return (
                self.day
                + self.start_time
                + self.end_time
                + self.course_code
                + self.room
            )
        else:
            return ""


class Instructor:
    def __init__(
        self,
        first_name=None,
        last_name=None,
        office=None,
        email=None,
        phone=None,
        office_hours=None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.office = office
        self.email = email
        self.phone = phone
        self.office_hours = office_hours  # list of OfficeHourTimeBlocks
        self.classes = classes # list of ClassTimeBlocks


class OfficeHourTimeBlock(TimeBlock):
    def __init__(self, is_class=False, is_office_hours=True):
        super().__init__(self)
        self.is_class = is_class
        self.is_office_hours = is_office_hours

class ClassTimeBlock(TimeBlock):
    def __init__(self, is_class=True, is_office_hours=False):
        super().__init__(self)
        self.is_class = is_class
        self.is_office_hours = is_office_hours

class Room:
    def __init__(self, campus = None, building = None, room_number = None):
        self.campus = campus
        self.building = building
        self.room_number = room_number

class Day:
    def __init__(self, in_arg):
        day_dict = {
            "Mon": "Monday",
            "Tues": "Tuesday",
            "Wed": "Wednesday",
            "Thurs": "Thursday",
            "Fri": "Friday",
            "Sat": "Saturday",
            "Sun": "Sunday",
        }
        num_dict = {
            1: "Mon",
            2: "Tues",
            3: "Wed",
            4: "Thurs",
            5: "Fri",
            6: "Sat",
            7: "Sun",
        }
        if type(in_arg) == int and in_arg in [1, 2, 3, 4, 5, 6, 7]:
            self.number = in_arg
            self.short_name = num_dict[in_arg]
            self.long_name = day_dict[self.short_name]
        elif in_arg in day_dict.keys():
            self.short_name = in_arg
            self.long_name = day_dict[in_arg]
        elif in_arg in day_dict.values():
            self.long_name = in_arg
        else:
            return TypeError(
                'Only 1-7, "Mon" or "Monday" can be used to create a Day object'
            )
