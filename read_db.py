# read_db.py

from models import TimeBlock, Instructor, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///sqlalchemy_example.db")
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
# Make a query to find all Time_Blocks in the database
# session.query(Time_Block).all()
time_block = session.query(TimeBlock).first()
print(time_block.CRN)
# CRN 11850
time_block = session.query(TimeBlock).all()
print(time_block)
# Find all Address whose person field is pointing to the person object
# session.query(Address).filter(Address.person == person).all()
# Retrieve one Address whose person field is point to the person object
# session.query(Address).filter(Address.person == person).one()
# address = session.query(Address).filter(Address.person == person).one()
#

instructor = session.query(Instructor).first()
print(instructor.first_name)
# instr_first_name = 'Peter'
instr_first_name = input("Enter instructor first name (include capital): ")
print(f"\nClasses for {instr_first_name}:")
for block in session.query(TimeBlock).filter(
    TimeBlock.instructor_first_name == instr_first_name
):
    print(
        f"{block.course_num} {block.day} {block.start_time} - {block.stop_time} {block.building}{block.room_number}"
    )
