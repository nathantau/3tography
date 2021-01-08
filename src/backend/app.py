from flask import Flask, request
from .helpers import s3, auth, pg
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hellofew"

@app.route('/upload', methods=['POST'])
def upload():
    '''
    Uploads the given image (png) to S3. The pos represents
    the 1st, 2nd or 3rd position on the UI.
    RESTRICT TO PNG!!!
    '''
    # CHECK IF USER IS AUTHENTICATED FIRST
    pass
    # Determine position to upload
    pos = request.json.get('pos')
    user = request.json.get('user')
    # Download image into /tmp/users directory
    image = request.files.get('File', '')
    image.save(f'/tmp/users/{user}/{pos}.png')
    # Upload to S3
    _, error = s3.upload_img(user, f'{pos}.png')
    if error:
        return json.dumps({
            'error': error
        })

    
@app.route('/register', methods=['POST'])
def register():
    pass

@app.route('/login', methods=['POST'])
def login():
    pass

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')