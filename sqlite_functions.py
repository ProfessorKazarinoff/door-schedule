# sqlite_functions.py
"""
Functions dealing with the sqlite database
"""

import os
import sqlite3
from sqlite3 import Error


def create_db(db_file):
    """ create a database connection to a SQLite database """
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
    """ create a database connection to the SQLite database
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
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    db = os.path.join(os.getcwd(), "out", "db.sqlite3")
    sql_create_time_block_table = """CREATE TABLE time_blocks (
                                        id integer PRIMARY KEY,
                                        course text NOT NULL,
                                        CRN text NOT NULL,
                                        start_time text NOT NULL,
                                        end_time text NOT NULL,
                                        term integer NOT NULL,
                                        year integer NOT NULL,
                                        location text NOT NULL,
                                        instructor text NOT NULL,
                                        FOREIGN KEY (instructor) REFERENCES instructors (id)
                                        );"""
    sql_create_instructors_table = """CREATE TABLE instructors (
                                    id integer PRIMARY KEY,
                                    first_name text NOT NULL,
                                    middle_name text,
                                    last_name text NOT NULL,
                                    departments text NOT NULL
                                );"""

    create_db(db)
    conn = create_connection(db)
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_time_block_table)

        # create tasks table
        create_table(conn, sql_create_instructors_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
