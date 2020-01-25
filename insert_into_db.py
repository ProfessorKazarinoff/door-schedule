# insert_into_db.py
"""
A working python script to insert a record into the the time_block database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import TimeBlock, Instructor, Base
import datetime
import maya
from sqlite_functions import create_sql_dict

from class_page_iter_tools import get_dept_urls, get_class_url_lst
from new_bs4_functions import pull_time_block_list_from_url
import run_new

engine = create_engine("sqlite:///sqlalchemy_example.db")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a time block into the time_blocks table
new_time_block = TimeBlock(CRN=13243, course_num="CMET133")
session.add(new_time_block)
session.commit()

# Insert an instructor in the instructors table
new_instructor = Instructor(first_name="peter")
session.add(new_instructor)
session.commit()

# Try a more complicated time_block insertion
t1 = datetime.time(9, 0, 0)
t2 = datetime.time(11, 50, 0)

d = {
    "CRN": 55555,
    "building": "AM",
    "campus": "SY",
    "course_num": "CMET211",
    "course_title": "Environmental Quality",
    "day": "Tuesday",
    "department": "CMET",
    "instructor_first_name": "Todd",
    "instructor_last_name": "Sanders",
    "room_number": "105",
    "start_time": t1,
    "stop_time": t2,
    "year": 2020,
    "quarter": 1,
}

another_time_block = TimeBlock(**d)
session.add(another_time_block)
session.commit()

# Try to add an instructor
instr_dict = {}
instr_dict["first_name"] = "Peter"
instr_dict["last_name"] = "Kazarinoff"
instr_dict["campus"] = "SY"
instr_dict["building"] = "SS"
instr_obj = Instructor(**instr_dict)
session.add(instr_obj)
session.commit()


# now to try something crazy
# url = "https://www.pcc.edu/schedule/default.cfm?fa=dspCourse2&thisTerm=202001&crsCode=ENGR&subjCode=ENGR&crsNum=211&topicCode=GE&subtopicCode=%20"

time_block_list = run_new.main()

for time_block_dict in time_block_list:
    sql_dict = create_sql_dict(time_block_dict)
    time_block = TimeBlock(**sql_dict)
    session.add(time_block)
    session.commit()


#    time_block_dict['CRN'] = crn_int
#    time_block_obj = Time_Block(**time_block_dict)
#    session.add(time_block_obj)
#    session.commit()

"""
{'CRN': '10475',
  'building': 'ST',
  'campus': 'SY',
  'course_num': 'ENGR222',
  'course_title': 'Electrical Circuits II',
  'day': 'Thursday',
  'department': 'ENGR',
  'instructor_first_name': 'Steve',
  'instructor_last_name': 'Haskell',
  'room_number': '313',
  'start_time': '1:00pm',
  'stop_time': '3:50pm'}
"""
