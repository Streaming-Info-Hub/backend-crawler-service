try:
    import sys,os
    from os.path import dirname, join, abspath
    import bs4
    from urllib.request import urlopen
    import sched, time
    import schedule

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

    from common_utils import common_crawler_util as crawler_util
    from common_utils.helpers import common_ut as CommonsUtils
    from datetime import datetime
    from common_utils.database import MySqlDB

except Exception as e:
    print("Some modules are not installed : {}".format(e))


URLS = [
    CommonsUtils.DeciderUrls.netflix[0],
    CommonsUtils.DeciderUrls.amazon[0], 
    CommonsUtils.DeciderUrls.hulu[0], 
    CommonsUtils.DeciderUrls.disney_plus[0], 
    CommonsUtils.DeciderUrls.hbo_max[0]
    ]
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
    print ('executing....new_streamings_crawler.......script....')
    try:
        print("***********running script on: %s ***********"% NOW.strftime("%d/%m/%Y %H:%M:%S"))
        for url in URLS:
            print("trying to connecting is url: %s" % url)
            page = urlopen(url)

            if page.status != 200:
                print("processing skipped:::: because url is not connected")
                break

            soup = bs4.BeautifulSoup(page, 'lxml')
            ''' 
            find all div elements that are inside a div element
            and are proceeded by an h3 element
            '''
            selector = 'h3'
            # find elements that contain the data we want
            found = soup.select(selector)
            # Extract data from the found elements
            data = [x.text.split(';')[-1].strip() for x in found]

            #number_of_elements = [3,4,5,6, 16, 17, 32, 33]

            for number in range (len(data)):
                print ("*"*60)
                print("Crawling data for number: %s"%number)
                platform = data[2]
                print("data found on : %s"% platform)
                name = data[number].split("(")
                name = name[0]

                if(name.split(" ")[0]=='Released'):
                    print("processs skipped:::: name data is not valid")
                    continue


                if "Released"  not in data[number]:
                    print("processs skipped:::: name data is not valid")
                    continue
                    
                released_date = data[number].split("(")
                released_date = released_date[1]
                released_date = released_date.split(" ")
                released_date = released_date[1] + ' ' + released_date[2].replace(')', '')

                #TODO:
                get_platform_id = ''

                insert_object = {
                    "uuid": CommonsUtils.generate_uuid4(),
                    "name": name,
                    "platform_name": platform.lower(),
                    "releases_date" : released_date,
                    "platform_id": 1,#TODO:
                    "status": 'active'
                }

                data_exist = DB.find_sql(
                                    table_name=crawler_util.config.get('tables', 'new_releases'),
                                    filters={
                                        'name': name
                                    }
                                )

                if data_exist:
                    print("processs skipped:::: because data is already exists on our database")
                    continue

                else:
                    insert_response = DB.insert_sql(table_name=crawler_util.config.get('tables', 'new_releases'),insert_data=insert_object) #TODO:
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