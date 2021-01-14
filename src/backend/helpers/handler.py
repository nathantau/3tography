import os, json, time
from flask import Response
import bcrypt

from .cors import modify_headers
from .users import update_image, image_links, user_exists, create_user, get_user, get_following, set_follow
from .s3 import upload_img, gen_presigned_url, refresh_url
from .auth import TokenHandler


SECRET_KEY = os.environ.get('SECRET_KEY') or 'DEFAULT_SECRET'
BYPASS_AUTH = {'/login', '/register', '/authenticated'}


def handle(request, path):
    try:
        if request.method == 'OPTIONS':
            return modify_headers(Response())
        return modify_headers(Response(json.dumps(flow(request, path))))
    except Exception as e:
        return modify_headers(Response(json.dumps({
            'reasonForFailure': str(e)
            }), status=500
        ))


def flow(request, path):
    path_to_handler = {
        '/upload': upload,
        '/me': me,
        '/login': login,
        '/register': register,
        '/following': following,
        '/follow': follow,
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
        return path_to_handler[path](request=request)


def upload(**kwargs):
    request = kwargs['request']
    # Determine position to upload
    pos = request.form.get('pos')
    user = kwargs['username']
    # Download image into /tmp/users directory
    image = request.files.get('File', '')
    directory = f'/tmp/users/{user}/'
    # Create directory if not already exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    image.save(f'{directory}/{pos}.png')
    # Upload to S3
    _, error = upload_img(user, f'{pos}.png')
    # Delete image's local copy
    os.remove(f'{directory}/{pos}.png')
    if error:
        return {
            'error': error
        }
    # Generate S3 presigned URL
    url = gen_presigned_url(user, pos)
    if not url:
        raise ValueError('Unable to generate presigned URL for uploaded image')
    # Update URL in PG
    _, error = update_image(user, pos, url)
    if error:
        raise ValueError(error)
    return {
        'status': f'Successfully uploaded image for {user}'
    }


def me(**kwargs):
    '''
    Retrieves S3 presigned URLs from DB and generates new ones if they are
    within an hour of expiration.
    '''
    user = kwargs['username']
    links = image_links(user)
    updated_links = list(links)
    filenames = ['one', 'two', 'three']
    for idx, link in enumerate(links):
        updated_links[idx] = refresh_url(user, filenames[idx], link)
    return {
        'user': user,
        'imageUrls': updated_links
    }


def register(**kwargs):
    '''
    Creates a new user in the database.
    '''
    request = kwargs['request']
    # Get user information
    username = request.json.get('user')
    password = request.json.get('password')
    if not username or not password:
        raise ValueError('Missing username or password')
    # Determine if user exists
    if user_exists(username):
        raise ValueError('User already exists')
    # Register user
    hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
    out, err = create_user(username, hashed_pw)
    if err:
        raise ValueError('Error inserting user into DB')
    return {
        'registered': True
    }


def login(**kwargs):
    '''
    Logs in a user and returns an authorization token.
    '''
    request = kwargs['request']
    # Get user information
    username = request.json.get('user')
    password = request.json.get('password')
    if not username or not password:
        return {
            'error': 'Missing username or password'
        }
    # Determine if user exists
    user_info = get_user(username)
    if not user_info:
        raise ValueError('User does not exist');
    # Login user and generate auth token
    if bcrypt.checkpw(password.encode('utf8'), user_info['password'].encode('utf8')):
        return {
            'success': True,
            'accessToken': TokenHandler.get_encoded_token(username, SECRET_KEY).decode('utf8')
        }
    return {
        'error': 'Unable to login'
    }


def follow(**kwargs):
    '''
    The user follows the specified user in the request.
    '''
    username = kwargs['username']
    request = kwargs['request']
    return {
        'followed': set_follow(username, request.json.get('user'))
    }


def following(**kwargs):
    '''
    Retrieves all following of the given account (with S3 URLs).
    '''

    username = kwargs['username']
    users = [me(username=user) for user in get_following(username)]
    return {
        'following': users
    }


def authenticated(**kwargs):
    request = kwargs['request']
    try:
        token = request.headers.get('Authorization')
        if not token or not TokenHandler.decode_token(token.replace('Bearer ', ''), SECRET_KEY):
            return {
                'authenticated': False
            }
        return {
            'authenticated': True
        }
    except Exception as e:
        return {
            'error': str(e)
        }
