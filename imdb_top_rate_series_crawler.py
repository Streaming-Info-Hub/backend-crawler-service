
try:
    from bs4 import BeautifulSoup
    import requests
    import re
    import sys,os
    from os.path import dirname, join, abspath
    import schedule, time


    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    from common_utils import common_crawler_util as crawler_util
    from common_utils.helpers import common_ut as CommonsUtils
    from datetime import datetime
    from common_utils.database import MySqlDB

except Exception as e:
    print("Some modules are not installed : {}".format(e))



URL = 'https://www.imdb.com/chart/tvmeter'  #TODO:

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
SLEEP_TIME = 600 #seconds


def crawler():
    print ('executing....imdb_top_rate_series_crawler.....script....')
    try:
        print("***********running script on: %s ***********"% NOW.strftime("%d/%m/%Y %H:%M:%S"))
        print("trying to connecting is url: %s" % URL)
        response = requests.get(URL)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            series_list = soup.select('td.titleColumn')
            images = soup.select('td.posterColumn')
            crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
            ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]

            # Store each item into dictionary (data), then put those into a list (imdb)
            for index in range(0, len(series_list)):

               

                # Seperate series into: 'place', 'title', 'year'
                series_string = series_list[index].get_text()
                series = series_string.split('(')
                series_title = series[0]
                year = re.search('\((.*?)\)', series_string).group(1)
                
                rank_number = index+1
                start_casts = ''
                if crew[index]:
                    start_casts = crew[index].split(',')[1:]
                    start_casts = ','.join(start_casts).replace("'", ' ')

                # for index_n  in range(0, len(images)):
                #     series_image_link = images[index_n].get('a')['href']
                #     print(series_image_link)


            
                # Insert into database
                insert_object = {
                    "uuid": CommonsUtils.generate_uuid4(),
                    "name": series_title.replace("'", ' '),
                    "release_date": year,
                    "rank_number" : rank_number,
                    "star_cast": start_casts,
                    "rating": float(ratings[index])
                }

                data_exist = DB.find_sql(
                                    table_name=crawler_util.config.get('tables', 'imdb_top_rate_series'),
                                    filters={
                                        'name': series_title
                                    }
                                )

                if data_exist:
                    print("processs skipped:::: because data is already exists on our database")
                    continue

                else:
                    print("Inserting series rank number is......: %s "%rank_number)
                    insert_response = DB.insert_sql(table_name=crawler_util.config.get('tables', 'imdb_top_rate_series'),insert_data=insert_object) #TODO:
                    if insert_response:
                        print("insert processed successfully the data is: %s"% insert_object)

        print("processing skipped:::: because url is not connected")

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