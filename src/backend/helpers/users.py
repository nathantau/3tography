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


def user_info(user):
    '''
    Returns None if user does not exist.
    '''
    cur, conn = create_connection()
    cur.execute(f'SELECT * FROM users WHERE username = \'{user}\'')
    info = cur.fetchone()
    close_connection(cur, conn)
    return info


def get_user(username):
    info = user_info(username)
    if not info:
        return None
    fields = ['username', 'password', 'followers', 'following', 'one', 'two', 'three', 'profile', 'description']
    return {
        fields[idx]: info[idx] for idx in range(len(fields))
    }


def image_links(username):
    user = get_user(username)
    if not user:
        return []
    return [user['one'], user['two'], user['three']]


def update_image(username, pos, url):
    if not user_exists(username):
        return False, 'User does not exist'
    success, err = update_user(username, pos, url)
    return success, err


def user_exists(username):
    return True if get_user(username) else False


def create_user(username, password):
    try:
        cur, conn = create_connection()
        cur.execute(
            'INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (username, password, [], [], '', '', '', '', '')
        )
        conn.commit()
        return True, None
    except Exception as e:
        return False, e


def update_user(username, column, value):
    try:
        cur, conn = create_connection()
        cur.execute(
            f'UPDATE users SET {column} = \'{value}\' WHERE username = \'{username}\''
        )
        conn.commit()
        return True, None
    except Exception as e:
        return False, e    


# def follow(user1, user2):
#     '''
#     Makes user1 follow user2.
#     '''
#     # Ensure both users exist
#     if not user_exists(user1) or not user_exists(user2):
#         return None, 'Specified user(s) do not exist'
#     # Update both user1 and user2 rows
#     query_str = '''
#         UPDATE users
#         SET following = array_append(following, '{}')
#         WHERE username = '{}'
#     '''.format(user2, user1)
#     out, err = query(query_str)
#     if err:
#         return None, 'Error updating following list {}'.format(str(err))
#     query_str = '''
#         UPDATE users
#         SET followers = array_append(followers, '{}')
#         WHERE username = '{}'
#     '''.format(user1, user2)
#     out, err = query(query_str)
#     return out, err


# def list_users():
#     query_str = '''
#         SELECT * FROM users
#     '''
#     out, err = query(query_str)
#     return out, err    


# def get_user(user):
#     query_str = f'''
#         SELECT * FROM users WHERE username = '{user}'
#     '''
#     out, err = query(query_str)
#     if err:
#         return None, f'Unable to query for user {user}'
#     if len(out) == 0:
#         return None, f'User {user} does not exist'
#     fields = ['username', 'password', 'followers', 'following', 'one', 'two', 'three', 'profile', 'description']
#     return {
#         fields[idx]: out[idx] for idx in range(len(fields))
#     }, None


def create_users_table():
    query_str = '''
        CREATE TABLE users (
            username text PRIMARY KEY,
            password text,
            followers text[],
            following text[],
            one text,
            two text,
            three text,
            profile_pic text,
            description text
        );
    '''
    out, err = query(query_str)
    return out, err
