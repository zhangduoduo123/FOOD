import os
from dotenv import load_dotenv
load_dotenv()  # 加载.env文件中的环境变量
host = os.environ.get('MYSQL_HOST')
port = int(os.environ.get('MYSQL_PORT'))
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('MYSQL_DATABASE')

MYSQL_CONFIG = {
    'host': host,
    'port': port,
    'user': user,
    'password': password,
    'database': database
}
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")