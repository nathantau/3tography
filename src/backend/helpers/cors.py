import os

def modify_headers(response):
    response.headers['Access-Control-Allow-Origin'] = os.environ.get('REACT_HOST')
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
