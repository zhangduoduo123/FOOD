import os

MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST'),
    'port': os.environ.get('MYSQL_PORT'),
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DATABASE')
}

MCP_OPTIMIZE_DUMPLING_DIR = os.environ.get("MCP_OPTIMIZE_DUMPLING_DIR")