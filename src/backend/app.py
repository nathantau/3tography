from flask import Flask, request, Response
from helpers import s3, auth, pg, users, cors, handler

import json
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    response = Response(json.dumps({
        'hello': 'world'
    }))
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return response


@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload():
    '''
    Uploads the given image (png) to S3. The pos represents
    the 1st, 2nd or 3rd position on the UI.
    RESTRICT TO PNG!!!
    '''
    return handler.handle(request, '/upload')

    
@app.route('/me', methods=['GET', 'OPTIONS'])
def me():
    # check if user exists
    return handler.handle(request, '/me')


@app.route('/register', methods=['POST', 'OPTIONS'])
def register():
    return handler.handle(request, '/register')


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    return handler.handle(request, '/login')


@app.route('/authenticated', methods=['GET', 'OPTIONS'])
def authenticated():
    return handler.handle(request, '/authenticated')


@app.route('/following', methods=['GET', 'OPTIONS'])
def following():
    return handler.handle(request, '/following')


@app.route('/search', methods=['GET', 'OPTIONS'])
def search():
    return handler.handle(request, '/search')


@app.route('/follow', methods=['POST', 'OPTIONS'])
def follow():
    return handler.handle(request, '/follow')


@app.route('/unfollow', methods=['POST', 'OPTIONS'])
def unfollow():
    return handler.handle(request, '/unfollow')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)