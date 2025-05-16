import os
import pymysql
MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST'),
    'port': os.environ.get('MYSQL_PORT'),
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DATABASE')
}

def get_mysql_connection():
    return pymysql.connect(**MYSQL_CONFIG)

