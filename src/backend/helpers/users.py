from .pg import query

def register(username):
    pass




def user_exists(username):
    query_str = '''
        SELECT COUNT(*) FROM users WHERE username = '{}'
    '''.format(username)
    out, err = query(query_str)
    return out[0][0] == '1'

def register(username, password):
    # Check if user exists
    if user_exists:
        return None, 'User already exists'
    # Add user
    query_str = '''
        INSERT INTO users VALUES
        ('', '{}', '{}', '{{}}', '{{}}')
    '''.format(username, password)
    out, err = query(query_str)
    return out, err    

def follow(user1, user2):
    '''
    Makes user1 follow user2.
    '''
    # Ensure both users exist
    if not user_exists(user1) or not user_exists(user2):
        return None, 'Specified user(s) do not exist'
    # Update both user1 and user2 rows
    query_str = '''
        UPDATE users
        SET following = array_append(following, '{}')
        WHERE username = '{}'
    '''.format(user2, user1)
    out, err = query(query_str)
    if err:
        return None, 'Error updating following list {}'.format(str(err))
    query_str = '''
        UPDATE users
        SET followers = array_append(followers, '{}')
        WHERE username = '{}'
    '''.format(user1, user2)
    out, err = query(query_str)
    return out, err

def list_users():
    query_str = '''
        SELECT * FROM users
    '''
    out, err = query(query_str)
    return out, err    

def create_users_table():
    query_str = '''
        CREATE TABLE users (
            google_id text,
            username text PRIMARY KEY,
            password text,
            followers text[],
            following text[],
            one text,
            two text,
            three text
        );
    '''
    out, err = query(query_str)
    return out, err
