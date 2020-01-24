# read_db.py

from models import Time_Block, Instructor, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///sqlalchemy_example.db")
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
# Make a query to find all Time_Blocks in the database
# session.query(Time_Block).all()
time_block = session.query(Time_Block).first()
print(time_block.CRN)
# CRN 11850
time_block = session.query(Time_Block).all()
print(time_block)
# Find all Address whose person field is pointing to the person object
# session.query(Address).filter(Address.person == person).all()
# Retrieve one Address whose person field is point to the person object
# session.query(Address).filter(Address.person == person).one()
# address = session.query(Address).filter(Address.person == person).one()
#

instructor = session.query(Instructor).first()
print(instructor.first_name)
