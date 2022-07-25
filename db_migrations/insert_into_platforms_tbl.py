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

insert_object_list = [
    {
    'id': 1,
    'uuid' : '4c0b3f82-fde6-11ec-ab79-c7ca8f4c2649',
    'name' : 'netflix',
    'logo' : 'https://i.ibb.co/QMnD2xN/Netflix-Logo.png',
    'description': 'netflix',
    'link' : 'netflix'
    },
     {
    'id': 2,
    'uuid' : 'bec7d8aa-fde6-11ec-8e21-aba366490df6',
    'name' : 'amazon',
    'logo' : 'https://i.ibb.co/gjHNW8Y/simple-vector-filled-flat-amazon-icon-logo-solid-black-pictogram-isolated-white-background-amazon-lo.jpg',
    'description': 'amazon',
    'link' : 'amazon'
    },
     {
    'id': 3,
    'uuid' : 'cbbee4e0-fde6-11ec-ad64-57640709c3c1',
    'name' : 'hulu',
    'logo' : 'https://i.ibb.co/q1D0HDP/download.png',
    'description': 'hulu',
    'link' : 'hulu'
    },
     {
    'id': 4,
    'uuid' : 'd07904e8-fde6-11ec-b47c-bbd775d7be59',
    'name' : 'disney_plus',
    'logo' : 'https://i.ibb.co/VVhBHPK/Disney-logo-svg.png',
    'description': 'disney_plus',
    'link' : 'disney_plus'
    },
     {
    'id': 5,
    'uuid' : 'd6c8ee1c-fde6-11ec-b491-4f69b0ee03c9',
    'name' : 'hbo_max',
    'logo' : 'https://i.ibb.co/3c4RmYq/HBO-Max-Logo.png',
    'description': 'hbo_max',
    'link' : 'hbo_max'
    },
     {
    'id': 6,
    'uuid' : 'e2952022-0c40-11ed-b240-bf9c657f1ac5',
    'name' : 'apple_tv_plus',
    'logo' : 'https://i.ibb.co/F6bSr2h/1280px-Apple-TV-Plus-Logo-svg.png',
    'description': 'apple_tv_plus',
    'link' : 'apple_tv_plus'
    }
]
for data in insert_object_list:
    insert_response = db.insert_sql(table_name=crawler_util.config.get('tables', 'platforms'),insert_data=data)
    if insert_response:
        print("Insert successfully the data is: %s"% data)
