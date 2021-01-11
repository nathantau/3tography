import os, json, time
from flask import Response


from .cors import modify_headers
from .users import update_image, image_links
from .s3 import upload_img, gen_presigned_url


def handle(request, path):
    if request.method == 'OPTIONS':
        return modify_headers(Response())
    path_to_handler = {
        '/upload': upload,
        '/me': me
    }
    if not path_to_handler.get(path):
        return modify_headers(Response(json.dumps({
            'error': 'Path does not exist'
        })))
    return modify_headers(Response(path_to_handler[path](request)))


def hello_world(request):
    return "hello"


def upload(request):
    # CHECK IF USER IS AUTHENTICATED/EXISTS FIRST
    pass
    # Determine position to upload
    pos = request.form.get('pos')
    user = request.form.get('user')
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
        return modify_headers(Response(
            json.dumps({
                'error': error
            })
        ))
    # Generate S3 presigned URL
    url = gen_presigned_url(user, pos)
    if not url:
        return json.dumps({
            'error': 'Unable to generate presigned URL for uploaded image'
        })
    # Update URL in PG
    _, error = update_image(user, pos, url)
    if error:
        return modify_headers(Response(
            json.dumps({
                'error': error
            })
        ))
    response = json.dumps({
        'status': f'Successfully uploaded image for {user}'
    })
    return response

def me(request):
    '''
    Retrieves S3 presigned URLs from DB and generates new ones if they are
    within an hour of expiration.
    '''
    user = request.json.get('user')
    links = image_links(user)
    updated_links = list(links)
    for idx, link in enumerate(links):
        # Check if link within hour of expiry
        if '&Expires=' not in link:
            continue
        unix_timestamp = int(link.split('&Expires=')[1])
        curr_timestamp = time.time()
        if unix_timestamp - curr_timestamp < 3600:
            # Update presigned URL
            mapping = ['one', 'two', 'three']
            updated_links[idx] = gen_presigned_url(user, mapping[idx])
    response = json.dumps({
        'profileUrl': '',
        'imageUrls': updated_links
    })
    return response