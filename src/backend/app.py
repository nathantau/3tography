from flask import Flask, request
from helpers import handler

import json
import os

app = Flask(__name__)


@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload():
    return handler.handle(request, '/upload')

    
@app.route('/api/me', methods=['GET', 'OPTIONS'])
def me():
    return handler.handle(request, '/me')


@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    return handler.handle(request, '/register')


@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    return handler.handle(request, '/login')


@app.route('/api/authenticated', methods=['GET', 'OPTIONS'])
def authenticated():
    return handler.handle(request, '/authenticated')


@app.route('/api/following', methods=['GET', 'OPTIONS'])
def following():
    return handler.handle(request, '/following')


@app.route('/api/search', methods=['GET', 'OPTIONS'])
def search():
    return handler.handle(request, '/search')


@app.route('/api/follow', methods=['POST', 'OPTIONS'])
def follow():
    return handler.handle(request, '/follow')


@app.route('/api/unfollow', methods=['POST', 'OPTIONS'])
def unfollow():
    return handler.handle(request, '/unfollow')


@app.route('/api/description', methods=['POST', 'OPTIONS'])
def description():
    return handler.handle(request, '/description')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)