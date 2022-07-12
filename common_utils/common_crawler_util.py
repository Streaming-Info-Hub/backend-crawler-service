from json import encoder
import sys, os
from os.path import dirname, join, abspath  

import configparser

from common_utils.helpers import common_ut as common_util
from common_utils import ref_string
from common_utils import ref_string, common_crawler_util as crawler_util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

conf_file = BASE_DIR+'/configuration.ini'
config = configparser.RawConfigParser()
config.read(conf_file)