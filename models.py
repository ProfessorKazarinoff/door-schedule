# models.py
"""
Models for sqlite3 database
"""

from sqlalchemy import Column, Sequence, Integer, String, DateTime, Time, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Global Variables
SQLITE = "sqlite"

# Table Names
TIME_BLOCKS = "time_blocks"
INSTRUCTORS = "instructors"

Base = declarative_base()


class Time_Block(Base):
    __tablename__ = "time_blocks"
    id = Column(Integer, Sequence("id_seq"), primary_key=True)
    CRN = Column(Integer)
    building = Column(String(2))
    campus = Column(String(2))
    course_num = Column(String(7))
    course_title = Column(String(50))
    day = Column(String(10))
    department = Column(String(4))
    instructor_first_name = Column(String(20))
    instructor_last_name = Column(String(20))
    room_number = Column(Integer)
    start_time = Column(Time)
    stop_time = Column(Time)
    year = Column(Integer)
    quarter = Column(Integer)

    def __repr__(self):
        return f"{self.id}, {self.course_num}"


class Instructor(Base):
    __tablename__ = "instructors"
    id = Column(Integer, Sequence("id_seq"), primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    campus = Column(String(2))
    building = Column(String(2))
    office_room_num: Column(String(5))
    phone: Column(String(12))

    def __repr__(self):
        return f"{self.id}, {self.last_name}"


engine = create_engine("sqlite:///sqlalchemy_example.db")
Base.metadata.create_all(engine)
