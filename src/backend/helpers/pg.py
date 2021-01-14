import psycopg2
import os


DB_NAME = os.environ.get('PGUSER')
DB_USER = os.environ.get('PGUSER')


def create_connection():
    try:
        connection = psycopg2.connect(f'dbname={DB_NAME} user={DB_USER}')
        cursor = connection.cursor()
        return cursor, connection
    except Exception as e:
        return False, e
    

def close_connection(cursor, connection):
    try:
        cursor.close()
        connection.close()
        return True, None
    except Exception as e:
        return False, e
