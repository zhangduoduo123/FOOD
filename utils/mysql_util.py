import os
import pymysql
from utils.env_info import MYSQL_CONFIG

def get_mysql_connection():
    return pymysql.connect(**MYSQL_CONFIG)

