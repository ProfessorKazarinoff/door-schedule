# sqlite_functions.py
"""
Functions dealing with the sqlite database
"""
import maya
import os
import sqlite3
from sqlite3 import Error
import datetime


def create_db(db_file):
    """create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_sql_dict(time_block_dict, year=2020, quarter=1):
    sql_dict = {}
    sql_dict["CRN"] = int(time_block_dict["CRN"])
    sql_dict["building"] = time_block_dict["building"][0:2]
    sql_dict["campus"] = time_block_dict["campus"][0:2]
    sql_dict["course_num"] = time_block_dict["course_num"][0:7]
    sql_dict["course_title"] = time_block_dict["course_title"]
    sql_dict["day"] = time_block_dict["day"]
    sql_dict["department"] = time_block_dict["department"][0:4]
    sql_dict["instructor_first_name"] = time_block_dict["instructor_first_name"]
    sql_dict["instructor_last_name"] = time_block_dict["instructor_last_name"]
    if time_block_dict["room_number"] == "Web":
        sql_dict["room_number"] = None
    else:
        sql_dict["room_number"] = int(time_block_dict["room_number"])
    sql_dict["instructor_first_name"] = time_block_dict["instructor_first_name"]
    try:
        maya_t1 = maya.when(time_block_dict["start_time"])
        sql_dict["start_time"] = datetime.time(
            maya_t1.hour, maya_t1.minute, maya_t1.second
        )
        maya_t2 = maya.when(time_block_dict["stop_time"])
        sql_dict["stop_time"] = datetime.time(
            maya_t2.hour, maya_t2.minute, maya_t2.second
        )
    except:
        sql_dict["start_time"] = None
        sql_dict["stop_time"] = None
    # insert end time
    sql_dict["year"] = year
    sql_dict["quarter"] = quarter

    return sql_dict

class TimeBlock:
    def __init__(self,time_block_dict):
        self.end_time = time_block_dict['end_time']
        self.start_time = time_block_dict['start_time']
        self.crn = time_block_dict['crn']
        self.department = time_block_dict['department']
        self.class_type = time_block_dict['class_type']
        self.location = time_block_dict['location']
        self.instructor = time_block_dict['instructor']
        self.day = time_block_dict['day']
        

def write_time_block_obj_to_db(conn,time_block_obj):
    conn.execute("INSERT INTO time_blocks VALUES (:end_time, :start_time, :crn, :department, :class_type, :location, :instructor, :day)", time_block_obj.__dict__)

def main():
    db = os.path.join(os.getcwd(), "out", "db.sqlite3")
    sql_create_time_block_table = """CREATE TABLE time_blocks (
                                        id integer PRIMARY KEY,
                                        CRN text NOT NULL,
                                        day text NOT NULL,
                                        start_time text NOT NULL,
                                        end_time text NOT NULL,
                                        department text NOT NULL,
                                        class_type text NOT NULL,
                                        location text NOT NULL,
                                        instructor text NOT NULL
                                        );"""
    sql_create_instructors_table = """CREATE TABLE instructors (
                                    id integer PRIMARY KEY,
                                    first_name text NOT NULL,
                                    middle_name text,
                                    last_name text NOT NULL
                                );"""

    create_db(db)
    conn = create_connection(db)
    if conn is not None:
        # create time_block table
        create_table(conn, sql_create_time_block_table)

        # create tasks table
        create_table(conn, sql_create_instructors_table)
        
        # a sample time block dictionary
        time_block_dict = {'day': 'Tuesday', 'end_time': '3:50pm', 'start_time': '1:00pm', 'crn': '31067', 'department': 'ENGR', 'class_type': 'Remote', 'location': 'Remote', 'instructor': 'Rekha D Rao'}
        # write the dictionary to the database
        t1 = TimeBlock(time_block_dict)
        write_time_block_obj_to_db(conn,t1)


    else:
        print("Error! cannot create the database connection.")




if __name__ == "__main__":
    main()
