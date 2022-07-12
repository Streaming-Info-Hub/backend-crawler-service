import sys,os
from os.path import dirname, join, abspath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from db_migrations import create_table_ut 
from common_utils.helpers import common_ut

# create_table_ut.create_table(common_ut.Query.creating_platforms_tbl)
# create_table_ut.create_table(common_ut.Query.new_releases_tbl)
# create_table_ut.create_table(common_ut.Query.imdb_top_rated_movies_tbl)
create_table_ut.create_table(common_ut.Query.imdb_top_rate_series_crawler_tbl)

