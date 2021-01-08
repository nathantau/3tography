'''
Wrapper module for AWS S3 functionalities.
'''

import boto3

BUCKET = 'threetography'
MAX_UPLOADS = 3

def gen_presigned_url(user, pos, exp=60*120):
    '''
    Generates a presigned url allowing any individual to access the given link for 2 hours.
    '''
    s3 = boto3.client('s3')
    try:
        key = f'users/{user}/{pos}'
        url = s3.generate_presigned_url('get_object', 
            Params={'Bucket': BUCKET, 'Key': key},
            ExpiresIn=exp
        )
        return url
    except Exception as e:
        print('[ERR] Error generating presigned url: {}'.format(str(e)))
        return None

def can_upload(user):
    '''
    Determines if user can upload any more images (under assumption that user exists,
    implying that a user subdirectory in S3 exists as well).
    Returns:
    can_upload (bool)
    '''
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET)
    # Number of uploads is equal to number of files - 1 for prefix entry
    num_uploads = len(list(bucket.objects.filter(Prefix='users/{}/'.format(user))))
    print('[LOG] Number of uploads for {}:'.format(user), num_uploads)
    return num_uploads < MAX_UPLOADS

def upload_img(user, filename):
    '''
    Checks to see if there are less than 3 images in
    the S3 Bucket subdirectory and if so, uploads the image.
    Returns:
    (succeeded, error)
    '''
    if not can_upload(user):
        print('[ERR] User {} exceeded total uploads'.format(user))
        return False, 'User {} exceeded total uploads'.format(user)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET)
    try:
        bucket.upload_file('/tmp/{}/{}'.format(user, filename), 'users/{}/{}'.format(user, filename))
        return True, None
    except Exception as e:
        return False, 'Error uploading file to S3 for user {}: {}'.format(user, str(e))
