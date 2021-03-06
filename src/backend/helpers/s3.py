'''
Wrapper module for AWS S3 functionalities.
'''

import boto3
import time


BUCKET = '3tography'
MAX_UPLOADS = 3
credentials = {}


def assume_role():
    ''' Assume the threetography role if access is expired '''
    sts = boto3.client('sts')
    response = sts.get_caller_identity()
    if 'assumed-role' not in response.get('Arn'):
        # Assume role if not already assumed
        response = sts.assume_role(
            RoleArn='arn:aws:iam::372123248858:role/threetography',
            RoleSessionName='FlaskSession',
            DurationSeconds=3600*8
        )
        # Update credentials
        global credentials
        credentials = response.get('Credentials')


def gen_presigned_url(username, pos, exp=3600*8):
    ''' Generates a presigned url allowing any individual to access the given link for 8 hours by default '''
    assume_role()
    role_session = boto3.Session(
        aws_access_key_id=credentials.get('AccessKeyId'),
        aws_secret_access_key=credentials.get('SecretAccessKey'),
        aws_session_token=credentials.get('SessionToken')
    )
    s3 = role_session.client('s3')
    try:
        key = f'users/{username}/{pos}.png'
        url = s3.generate_presigned_url('get_object', 
            Params={'Bucket': BUCKET, 'Key': key},
            ExpiresIn=exp
        )
        return url
    except Exception as e:
        print('[ERR] Error generating presigned url: {}'.format(str(e)))
        return None


def refresh_url(user, pos, link):
    ''' Regenerates and returns an S3 presigned URL if it is within an hour of expiry '''
    if not link:
        return False, ''
    if '&Expires=' not in link:
        return False, ''
    unix_timestamp = int(link.split('&Expires=')[1])
    curr_timestamp = time.time()
    if unix_timestamp - curr_timestamp < 3600:
        return True, gen_presigned_url(user, pos, exp=3600*8)
    return False, link


def upload_image(user, filename):
    ''' Uploads a given image for a specified user in S3 '''
    assume_role()
    role_session = boto3.Session(
        aws_access_key_id=credentials.get('AccessKeyId'),
        aws_secret_access_key=credentials.get('SecretAccessKey'),
        aws_session_token=credentials.get('SessionToken')
    )
    s3 = role_session.resource('s3')
    bucket = s3.Bucket(BUCKET)
    try:
        bucket.upload_file('/tmp/users/{}/{}'.format(user, filename), 'users/{}/{}'.format(user, filename))
        return True, None
    except Exception as e:
        return False, 'Error uploading file to S3 for user {}: {}'.format(user, str(e))

