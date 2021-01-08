from flask import Flask, request
from helpers import s3, auth, pg, users

import json
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello world"

@app.route('/upload', methods=['POST'])
def upload():
    '''
    Uploads the given image (png) to S3. The pos represents
    the 1st, 2nd or 3rd position on the UI.
    RESTRICT TO PNG!!!
    '''
    # CHECK IF USER IS AUTHENTICATED /EXISTS FIRST
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
    _, error = s3.upload_img(user, f'{pos}.png')
    if error:
        return json.dumps({
            'error': error
        })
    # Generate S3 presigned URL
    url = s3.gen_presigned_url(user, pos)
    if not url:
        return json.dumps({
            'error': 'Unable to generate presigned URL for uploaded image'
        })
    # Update URL in PG
    _, error = users.update_image(user, pos, url)
    if error:
        return json.dumps({
            'error': error
        })
    return json.dumps({
        'status': f'Successfully uploaded image for {user}'
    })
    
@app.route('/register', methods=['POST'])
def register():
    pass

@app.route('/login', methods=['POST'])
def login():
    pass

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')