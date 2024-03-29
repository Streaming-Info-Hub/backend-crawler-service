import os, sys
from os.path import dirname, join, abspath
import uuid 

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

def get_error_traceback(sys, e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return "%s || %s || %s || %s" %(exc_type, fname, exc_tb.tb_lineno,e)

def generate_uuid4():
    return str(uuid.uuid4()) 
class DeciderUrls:
    netflix = "https://decider.com/article/new-on-netflix/",
    amazon = "https://decider.com/article/new-on-amazon-prime/",
    disney_plus = "https://decider.com/article/new-on-disney-plus",
    hbo_max = "https://decider.com/article/new-on-hbo",
    hulu = "https://decider.com/article/new-on-hulu",

class Query:
    creating_platforms_tbl = '''
                                CREATE TABLE platforms (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                uuid VARCHAR(200),
                                name VARCHAR(42),
                                logo VARCHAR(500),
                                description VARCHAR(1000),
                                link  VARCHAR(300),
                                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                            );
                            
                            '''
    new_releases_tbl = '''
                                CREATE TABLE new_releases (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                uuid VARCHAR(200),
                                name VARCHAR(500),
                                releases_date VARCHAR(500),
                                platform_name VARCHAR(500),
                                platform_id INT,
                                status VARCHAR(200),
                                link  VARCHAR(500),
                                image VARCHAR(500),
                                streaming_status VARCHAR(200),
                                description VARCHAR(500),
                                deleted int DEFAULT 0,
                                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                            );
                            
                            '''


    imdb_top_rated_movies_tbl = '''
                                    CREATE TABLE imdb_top_rated_movies (
                                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    uuid VARCHAR(200),
                                    name VARCHAR(500),
                                    release_date VARCHAR(500),
                                    rank_number VARCHAR(500),
                                    director VARCHAR(500),
                                    star_cast VARCHAR(1000),
                                    status VARCHAR(200) DEFAULT 'active',
                                    link  VARCHAR(500),
                                    image VARCHAR(500),
                                    rating FLOAT,
                                    description VARCHAR(500),
                                    deleted int DEFAULT 0,
                                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                                );

                        '''

    imdb_top_rate_series_crawler_tbl = '''
                                    CREATE TABLE imdb_top_rate_series (
                                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    uuid VARCHAR(200),
                                    name VARCHAR(500),
                                    release_date VARCHAR(500),
                                    rank_number VARCHAR(500),
                                    star_cast VARCHAR(1000),
                                    status VARCHAR(200) DEFAULT 'active',
                                    link  VARCHAR(500),
                                    image VARCHAR(500),
                                    rating FLOAT,
                                    description VARCHAR(500),
                                    deleted int DEFAULT 0,
                                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                                );

                        '''

    admin_tbl = '''
                                    CREATE TABLE admin (
                                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    uuid VARCHAR(200),
                                    email VARCHAR(500),
                                    password VARCHAR(500),
                                    type VARCHAR(200),
                                    deleted int DEFAULT 0,
                                    two_fa_enabled tinyint DEFAULT 0,
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                                );

                        '''
                        
    login_session_tb = '''
                                        CREATE TABLE login_session (
                                        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                        uuid VARCHAR(200),
                                        token text,
                                        user_id int,
                                        session_expiry_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
                                        deleted int DEFAULT 0,
                                        ip VARCHAR(200),
                                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                                    );

                            '''

    current_streaming_movies_tbl = '''
                                CREATE TABLE current_streaming_movies (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                uuid VARCHAR(200),
                                name VARCHAR(500),
                                platform_name VARCHAR(500),
                                status VARCHAR(200),
                                genres VARCHAR(400),
                                link  VARCHAR(500),
                                image VARCHAR(500),
                                description VARCHAR(500),
                                deleted int DEFAULT 0,
                                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                            );
                            
                            '''


    current_streaming_series_tbl = '''
                                CREATE TABLE current_streaming_series (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                uuid VARCHAR(200),
                                name VARCHAR(500),
                                platform_name VARCHAR(500),
                                status VARCHAR(200),
                                genres VARCHAR(400),
                                start_date VARCHAR(300),
                                link  VARCHAR(500),
                                image VARCHAR(500),
                                description VARCHAR(500),
                                deleted int DEFAULT 0,
                                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                            );
                            
                            '''

    comming_soon_movies_tbl = '''
                                    CREATE TABLE comming_soon_movies (
                                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    uuid VARCHAR(200),
                                    name VARCHAR(500),
                                    status VARCHAR(200),
                                    genres VARCHAR(400),
                                    link  VARCHAR(500),
                                    image VARCHAR(500),
                                    description VARCHAR(500),
                                    deleted int DEFAULT 0,
                                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                                );
                                
                                '''

    tonight_streaming_series_tbl = '''
                                    CREATE TABLE tonight_streaming_series (
                                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    uuid VARCHAR(200),
                                    name VARCHAR(500),
                                    platform_name VARCHAR(500),
                                    status VARCHAR(200),
                                    start_date VARCHAR(300),
                                    link  VARCHAR(500),
                                    image VARCHAR(500),
                                    description VARCHAR(500),
                                    deleted int DEFAULT 0,
                                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                                );
                                
                                '''


    most_popular_series_tbl = '''
                                    CREATE TABLE most_popular_series (
                                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    uuid VARCHAR(200),
                                    unique_id BIGINT,
                                    name VARCHAR(500),
                                    platform_name VARCHAR(500),
                                    status VARCHAR(200),
                                    streaming_status VARCHAR(400),
                                    start_date VARCHAR(300),
                                    end_date VARCHAR(300),
                                    country VARCHAR(300),
                                    permalink VARCHAR(400),
                                    link  VARCHAR(500),
                                    image VARCHAR(500),
                                    description VARCHAR(500),
                                    deleted int DEFAULT 0,
                                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                                );
                                
                                '''