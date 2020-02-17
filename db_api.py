import sqlite3
from sqlite3 import Error
import os
from datetime import datetime
from time import strftime

# Global variable declaration
DB_FILE = str(os.getcwd()) + "/tour_data.db"


def connect_to_database():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param: None
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
    except Error as e:
        print(e)
    return conn


def select_tour_packages():
    """
    Show all the tours which are provided by the company
    """
    con = connect_to_database()
    cur = con.cursor()
    try:
        cur.execute(r"SELECT * FROM tour_data_table")
        rows = cur.fetchall()
        return rows
    except Error as err:
        print("Error while accessing data base " + str(err))


def select_tour_based_on_dates(start_date, end_date):
    """
    Database function to get the trip data based on user dates
    """
    con = connect_to_database()
    cur = con.cursor()
    formatted_start_date = datetime.strptime(start_date, '%d-%m-%Y').strftime('%d/%m/%Y')
    formatted_end_date = datetime.strptime(end_date, '%d-%m-%Y').strftime('%d/%m/%Y')
    try:
        cur.execute(r"SELECT * FROM tour_data_table where start_date >= ? "
                    r"and end_date <= ?", (formatted_start_date,
                                           formatted_end_date,))
        rows = cur.fetchall()
        return rows
    except Error as err:
        print("Error while accessing data base " + str(err))

