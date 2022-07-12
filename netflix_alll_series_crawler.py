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



URL = 'https://www.imdb.com/list/ls026838481/'  #TODO:

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

def parse_table(table): 
    head_body = {'head':[], 'body':[]}
    for tr in table.cssselect('tr'): 
        if all(t.tag == 'th' for t in tr.getchildren()): 
            head_body['head'] += [tr]
        else: 
            head_body['body'] += [tr]
    return head_body 


def crawler():
    print ('executing....imdb_top_chart_crawler.....script....')
    try:
        print("***********running script on: %s ***********"% NOW.strftime("%d/%m/%Y %H:%M:%S"))
        print("trying to connecting is url: %s" % URL)
        response = requests.get(URL)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
       
            #movies = soup.find('div',attrs={'class':'lister-list'})

            for teams in soup.find_all('div',attrs={'class':'lister-list'}):
                for team_a in teams.find_all("a"):
                    print(team_a.text)


            links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
            crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
            ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
            votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

            # Store each item into dictionary (data), then put those into a list (imdb)
            for index in range(0, len(movies)):
                # Seperate movie into: 'place', 'title', 'year'
                movie_string = movies[index].get_text()
                movie = (' '.join(movie_string.split()).replace('.', ''))
                movie_title = movie[len(str(index))+1:-7].replace("'", ' ')
                year = re.search('\((.*?)\)', movie_string).group(1)
                place = movie[:len(str(index))-(len(movie))]

                start_casts = crew[index].split(',')[1:]
                start_casts = ','.join(start_casts).replace("'", ' ')

            
                # Insert into database
                insert_object = {
                    "uuid": CommonsUtils.generate_uuid4(),
                    "name": movie_title,
                    "release_date": year,
                    "rank_number" : place,
                    "director":  crew[index].split(',')[0].replace('(dir.)', ' ').replace("'", ' '),
                    "star_cast": start_casts,
                    "rating": float(ratings[index])
                }

                data_exist = DB.find_sql(
                                    table_name=crawler_util.config.get('tables', 'imdb_top_rated_movies'),
                                    filters={
                                        'name': movie_title
                                    }
                                )

                if data_exist:
                    print("processs skipped:::: because data is already exists on our database")
                    continue

                else:
                    print("Inserting movie rank number is......: %s "%place)
                    insert_response = DB.insert_sql(table_name=crawler_util.config.get('tables', 'imdb_top_rated_movies'),insert_data=insert_object) #TODO:
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