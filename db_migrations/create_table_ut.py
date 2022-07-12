import sys,os
from os.path import dirname, join, abspath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from common_utils import common_crawler_util as crawler_util
from db_migrations import db_conf as db_connection

def create_table(query):
    try:
        print("Executing query for creating table")
        db_response = db_connection.db.create_sql_qry(query)

        if db_response:
            print("table created succcessfully")
            return True

        return False
    except:
        print("Error when executing query: %s "% query)