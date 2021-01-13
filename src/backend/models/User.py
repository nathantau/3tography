import psycopg2
import os


DB_NAME = os.environ.get('PGUSER')
DB_USER = os.environ.get('PGUSER')


class User():

    @staticmethod
    def create_table():
        pass


    @staticmethod
    def operate(method, params, query):
        '''
        Performs the given query.
        '''
        try:
            connection = psycopg2.connect(f'dbname={DB_NAME} user={DB_USER}')
            cursor = connection.cursor()
            cursor.execute(query, params)
            if method.lower() == 'select':
                info = cursor.fetchall()
            return info
        except Exception as e:
            return False


    def __init__(self, user, password):
        pass

    
    def get_images(self, user):
        User


    def update_image(self, user):
        pass


    def get_user(self, user):
        query = f'select * from users where user = \'{user}\''
        return User.operate('select', None, query)


    def operate(self):
        pass









conn = psycopg2.connect("dbname=nathan user=nathan")
cur = conn.cursor()
cur.execute("select * from users;")
print(cur.fetchall())
# try:
#     cur.execute("insert into users values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#     ("sam","$2b$12$bm5fBwc.DKLPbVuMQgDRK.VrUYT779b2.AXrXwvQeZeCRYn5a0n8S",[],[],"","","","",""))
#     conn.commit()
#     print(cur.fetchall())

# except Exception as e:
#     print(e)