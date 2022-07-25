try:
    import sys,os
    from os.path import dirname, join, abspath
    import bs4
    from urllib.request import urlopen
    import sched, time
    import schedule
    import requests
    import json
    import ast
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

    from common_utils import common_crawler_util as crawler_util
    from common_utils.helpers import common_ut as CommonsUtils
    from datetime import datetime
    from common_utils.database import MySqlDB

except Exception as e:
    print("Some modules are not installed : {}".format(e))


URL = "https://www.episodate.com/api/most-popular?page=%s"

DB = MySqlDB.MysqlDatabase(False, **{
        'mysql_pool_name': crawler_util.config.get('mysql', 'pool_name'),
        'mysql_pool_size': crawler_util.config.get('mysql', 'pool_size'),
        'mysql_host': crawler_util.config.get('mysql', 'host'),
        'mysql_port': crawler_util.config.get('mysql', 'port'),
        'mysql_user': crawler_util.config.get('mysql', 'user'),
        'mysql_password': crawler_util.config.get('mysql', 'password'),
        'database_name': crawler_util.config.get('mysql', 'database_name')
    })

NOW = datetime.now()
SLEEP_TIME = 10 #seconds

def parse_dictionary(data):
    return (ast.literal_eval(data))  



def crawler():
    print ('executing....most_popular_series_crawler.......script....')
    try:
        print("***********running script on: %s ***********"% NOW.strftime("%d/%m/%Y %H:%M:%S"))
        headers = {
            "authority": "www.rottentomatoes.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
            }
        page =1
        response = requests.get(URL%(page), headers=headers)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            result = json.loads(data)
            page_numbers = range(result.get("pages", 1088))
            for page in page_numbers:
                response = requests.get(URL%(page), headers=headers)
                if response.status_code == 200:
                    data = response.content.decode('UTF-8')
                    result = json.loads(data)

                    list = result.get("tv_shows")

                    for final_data in list:
                        insert_object = {
                            "uuid": CommonsUtils.generate_uuid4(),
                            "unique_id": final_data.get("id") or "Null",
                            "name": final_data.get("name", "").replace("'", " "),
                            "permalink": final_data.get("permalink") or "Null",
                            "start_date": final_data.get("start_date")or "Null",
                            "end_date": final_data.get("start_date")or "Null",
                            "country": final_data.get("country")or "Null",
                            "platform_name": final_data.get("network", "").lower(),
                            "streaming_status": final_data.get("status")or "Null",
                            "image": final_data.get("image_thumbnail_path")or "Null",
                            "status": "active"
                        }

                        data_exist = DB.find_sql(
                                            table_name=crawler_util.config.get('tables', 'most_popular_series'),
                                            filters={
                                                'name': final_data.get("name")
                                            }
                                        )

                        if data_exist:
                            print("processs skipped:::: because data is already exists on our database")
                            continue

                        else:
                            insert_response = DB.insert_sql(table_name=crawler_util.config.get('tables', 'most_popular_series'),insert_data=insert_object) #TODO:
                            if insert_response:
                                print("insert processed successfully the data is: %s"% insert_object) 

    except Exception as e:
            error =  CommonsUtils.get_error_traceback(sys, e)
            print("Erroe message is : %s"%error)
    finally:
        print("crawler execute successfully on: %s"% NOW.strftime("%d/%m/%Y %H:%M:%S"))

crawler()
while True:
    print ("*"*60)
    print ("*"*60)
    print ("*"*60)
    print ('The Next Syncs is happened after .......%s Seconds'%SLEEP_TIME)
    schedule.run_pending()
    time.sleep(SLEEP_TIME)
    crawler()
