import os, json, time
from flask import Response
import bcrypt


from .cors import modify_headers
from .users import update_image, create_user, get_user, get_following, set_follow, get_similar_usernames, set_unfollow, update_description
from .s3 import upload_image, gen_presigned_url, refresh_url
from .auth import TokenHandler


SECRET_KEY = os.environ.get('SECRET_KEY') or 'DEFAULT_SECRET'
BYPASS_AUTH = {'/login', '/register'}


def handle(request, path):
    ''' Abstracts CORS and errors '''
    try:
        if request.method == 'OPTIONS':
            return modify_headers(Response())
        return modify_headers(Response(json.dumps(flow(request, path))))
    except Exception as error:
        return modify_headers(Response(
            json.dumps({
                'reasonForFailure': str(error)
            }), status=500
        ))


def flow(request, path):
    ''' High-level encapsulation of route-handling '''
    path_to_handler = {
        '/login': login,
        '/register': register,
        '/upload': upload,
        '/me': me,
        '/following': following,
        '/follow': follow,
        '/unfollow': unfollow,
        '/search': search,
        '/description': description,
        '/authenticated': authenticated
    }
    if path not in path_to_handler:
        raise KeyError('Request path does not exist')
    token = request.headers.get('Authorization')
    if path not in BYPASS_AUTH:
        # Validate access token
        if not token:
            raise Exception('Missing access token', request.headers)
        if not TokenHandler.decode_token(token.replace('Bearer ', ''), secret_key=SECRET_KEY):
            raise Exception('Unable to decode access token')
        decoded_token = TokenHandler.decode_token(token.replace('Bearer ', ''), secret_key=SECRET_KEY)
        username = decoded_token['sub']
        return path_to_handler[path](request=request, username=username)
    else:
        # Skip authentication
        return path_to_handler[path](request=request)


def upload(**kwargs):
    ''' Uploads an image into S3 and retrieves its presigned URL '''
    request = kwargs['request']
    username = kwargs['username']
    pos = request.form.get('pos')
    # Download image into /tmp/users directory
    image = request.files.get('File', '')
    directory = f'/tmp/users/{username}/'
    # Create directory if not already exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    image.save(f'{directory}/{pos}.png')
    # Upload to S3
    _, error = upload_image(username, f'{pos}.png')
    # Delete image's local copy
    os.remove(f'{directory}/{pos}.png')
    if error:
        raise ValueError(error)
    # Generate S3 presigned URL
    url = gen_presigned_url(username, pos)
    if not url:
        raise ValueError('Unable to generate presigned URL for uploaded image')
    # Update URL in DB
    _, error = update_image(username, pos, url)
    if error:
        raise ValueError(error)
    return {
        'uploaded': True
    }


def me(**kwargs):
    '''
    Retrieves S3 presigned URLs from DB and generates new ones if they are
    within an hour of expiration. Also saves the new URLs in the database
    '''
    username = kwargs['username']
    # Get current user information and current URLs
    user = get_user(username)
    filenames = ['one', 'two', 'three']
    links = [user[filename] for filename in filenames]
    updated_links = list(links)
    for idx, link in enumerate(links):
        # Generate new URL if required
        updated, link = refresh_url(username, filenames[idx], link)
        if not updated:
            continue
        # Save URL in database
        _, error = update_image(username, filenames[idx], link)
        if error:
            continue
        updated_links[idx] = link
    return {
        'user': username,
        'imageUrls': updated_links,
        'description': user['description']
    }


def register(**kwargs):
    ''' Creates a new user in the database '''
    request = kwargs['request']
    # Get user information
    username = request.json.get('user')
    password = request.json.get('password')
    if not username or not password:
        raise ValueError('Missing username or password')
    # Determine if user exists
    if get_user(username):
        raise ValueError('User already exists')
    # Register user
    hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
    _, error = create_user(username, hashed_pw)
    if error:
        raise ValueError('Error inserting user into DB')
    return {
        'registered': True
    }


def login(**kwargs):
    ''' Logs in a user and returns an access token '''
    request = kwargs['request']
    # Get user information
    username = request.json.get('user')
    password = request.json.get('password')
    if not username or not password:
        raise ValueError('Missing username or password')
    # Determine if user exists
    user_info = get_user(username)
    if not user_info:
        raise ValueError('User does not exist');
    # Login user and generate auth token
    if bcrypt.checkpw(password.encode('utf8'), user_info['password'].encode('utf8')):
        return {
            'accessToken': TokenHandler.get_encoded_token(username, SECRET_KEY).decode('utf8')
        }
    raise ValueError('Incorrect credentials')


def follow(**kwargs):
    ''' The user follows the specified user in the request '''
    username = kwargs['username']
    request = kwargs['request']
    return {
        'followed': set_follow(username, request.json.get('user'))
    }


def unfollow(**kwargs):
    ''' The user follows the specified user in the request '''
    username = kwargs['username']
    request = kwargs['request']
    return {
        'unfollowed': set_unfollow(username, request.json.get('user'))
    }


def following(**kwargs):
    ''' Retrieves all following of the given account (with S3 URLs) '''
    username = kwargs['username']
    users = [me(username=user) for user in set(get_following(username))]
    return {
        'following': users
    }


def authenticated(**kwargs):
    ''' If the control flow even gets here then they are authenticated '''
    return {
        'authenticated': True
    }


def search(**kwargs):
    ''' Returns usernames in the DB similar to the passed in username '''
    username = kwargs['username']
    request = kwargs['request']
    to_search = request.args.get('user')
    if not to_search:
        raise ValueError('No user passed in')
    return {
        'results': get_similar_usernames(to_search)
    }


def description(**kwargs):
    ''' Updates the description of a user in the DB '''
    username = kwargs['username']
    request = kwargs['request']
    description = request.json.get('description')
    if description is None:
        raise ValueError('No description specified')
    return {
        'updated': update_description(username, description)
    }

