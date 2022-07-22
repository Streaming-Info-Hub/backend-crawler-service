import sys,os
from os.path import dirname, join, abspath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from common_utils import common_crawler_util as crawler_util

from common_utils.database import MySqlDB
from db_migrations import db_conf as db_connection

db = MySqlDB.MysqlDatabase(False, **{
        'mysql_pool_name': crawler_util.config.get('mysql', 'pool_name'),
        'mysql_pool_size': crawler_util.config.get('mysql', 'pool_size'),
        'mysql_host': crawler_util.config.get('mysql', 'host'),
        'mysql_port': crawler_util.config.get('mysql', 'port'),
        'mysql_user': crawler_util.config.get('mysql', 'user'),
        'mysql_password': crawler_util.config.get('mysql', 'password'),
        'database_name': crawler_util.config.get('mysql', 'database_name')
    })

insert_object = {
    'uuid' : 'db3896ae-03e1-11ed-abde-17e87d1f0144',
    'email' : crawler_util.config.get('mysql', 'admin_email'),
    'password' : crawler_util.config.get('mysql', 'admin_password'),
    'type': 'super_admin'
}


insert_response = db.insert_sql(table_name=crawler_util.config.get('tables', 'admin'),insert_data=insert_object)
if insert_response:
    print("Insert successfully the data is: %s"% insert_object)
