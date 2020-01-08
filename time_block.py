# time_block.py


class TimeBlock:
    def __init__(self, course_code, **kwargs):
        self.course_code = course_code
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return " ".join(
            [
                self.course_code,
                self.year,
                self.quarter,
                self.start_time,
                self.end_time,
                self.room_code,
            ]
        )
