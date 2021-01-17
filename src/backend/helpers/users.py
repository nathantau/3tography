from .pg import create_connection, close_connection


def get_user(username):
    ''' Returns an object representation of a user, None if it does not exist '''
    cur, conn = create_connection()
    cur.execute(f'SELECT * FROM users WHERE username = \'{username}\'')
    info = cur.fetchone()
    close_connection(cur, conn)
    if not info:
        return None
    fields = ['username', 'password', 'followers', 'following', 'one', 'two', 'three', 'profile', 'description']
    return {
        fields[idx]: info[idx] for idx in range(len(fields))
    }


def get_following(username):
    ''' Returns a list of usernames of the accounts the user is following '''
    user = get_user(username)
    if not user:
        return []
    return user.get('following') if user.get('following') else []


def image_links(username):
    '''
    Returns the S3 URLs of the user's images.
    '''
    user = get_user(username)
    if not user:
        return []
    return [user['one'], user['two'], user['three']]


def update_image(username, pos, url):
    if not get_user(username):
        return False, 'User does not exist'
    success, err = update_user(username, pos, url)
    return success, err


def create_user(username, password):
    try:
        cur, conn = create_connection()
        cur.execute(
            'INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (username, password, [], [], '', '', '', '', '')
        )
        conn.commit()
        close_connection(cur, conn)
        return True, None
    except Exception as e:
        return False, e


def update_user(username, column, value, is_array=False):
    try:
        cur, conn = create_connection()
        if is_array:
            cur.execute(
                'UPDATE users SET {} = array_append({}, %s)'.format(column, column),
                (value, )
            )
        else:
            cur.execute(
                f'UPDATE users SET {column} = \'{value}\' WHERE username = \'{username}\''
            )
        conn.commit()
        close_connection(cur, conn)
        return True, None
    except Exception as e:
        return False, e


def set_follow(username1, username2):
    '''
    Makes user1 follow user2.
    '''
    if not get_user(username1) or not get_user(username2):
        raise ValueError('Specified user(s) do not exist')
    user = get_user(username=username1)
    if username2 in set(user['following']):
        raise ValueError('User is already being followed')
    success, err = update_user(username1, 'following', username2, is_array=True)
    if err:
        raise ValueError(err)
    return True


def set_unfollow(username1, username2):
    ''' Makes user1 unfollow user2 '''
    if not get_user(username1) or not get_user(username2):
        raise ValueError('Specified user(s) do not exist')
    user = get_user(username=username1)
    if username2 not in set(user['following']):
        raise ValueError('User is not being followed')
    user['following'].remove(username2)
    cur, conn = create_connection()
    cur.execute(
        f'UPDATE users SET following = %s WHERE username = \'{username1}\'',
        (user['following'], )
    )
    conn.commit()
    close_connection(cur, conn)
    return True


def get_similar_usernames(username):
    ''' Retrieves all usernames like ${username}(.)* '''
    cur, conn = create_connection()
    cur.execute(f'SELECT username FROM users WHERE username LIKE \'{username}%\'')
    similar_usernames = list([item[0] for item in cur.fetchall()])
    close_connection(cur, conn)
    return similar_usernames


def update_description(username, description):
    ''' Updates the description of a given user '''
    # Escape single quotes in SQL by doubling up
    description = description.replace('\'', '\'\'')
    success, error = update_user(username, 'description', description)
    if error:
        raise ValueError(error)
    return True


# LEGACY
# def create_users_table():
#     query_str = '''
#         CREATE TABLE users (
#             username text PRIMARY KEY,
#             password text,
#             followers text[],
#             following text[],
#             one text,
#             two text,
#             three text,
#             profile_pic text,
#             description text
#         );
#     '''
#     out, err = query(query_str)
#     return out, err
