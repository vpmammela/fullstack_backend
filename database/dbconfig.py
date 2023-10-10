import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fullstack',
}

def get_database_connection():
    try:
        db_config = DB_CONFIG
        connection = mysql.connector.connect(**db_config)
        print(connection)
        return connection
    except Exception as error:
        raise error