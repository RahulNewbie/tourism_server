import csv
import sqlite3
import os

# Global variable declaration
DB_FILE = str(os.getcwd()) + "/tour_data.db"


def tour_planner():
    """
    Read the CSV file and insert records in Database
    """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("CREATE TABLE tour_data_table (id,start_date,end_date,destination,"
                "price,desc,type,risk_factor);")
    with open('tour_data.csv', 'rt') as fin:
        # csv.DictReader read line by line
        dr = csv.DictReader(fin)
        to_db = [(i['id'], i['start_date'], i['end_date'],
                  i['destination'], i['price'], i['desc'],
                  i['type'], i['risk_factor']) for i in dr]

    cur.executemany("INSERT INTO tour_data_table "
                    "(id,start_date,end_date,destination,price,"
                    "desc,type,risk_factor) "
                    "VALUES (?, ?, ?, ?,?, ?, ?, ?);", to_db)
    print("database insertion finished")
    con.commit()
    con.close()


if __name__ == "__main__":
    tour_planner()
