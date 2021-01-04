from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hellofew"

@app.route('/add', methods=['POST'])
def add():
    pass

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')