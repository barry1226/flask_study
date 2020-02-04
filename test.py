from flask import Flask, escape, url_for, render_template, request
app = Flask(__name__)

app.debug = True

@app.route('/hi/')
def hello_world():
    return 'Hello World'

@app.route('/hi/<username>/')
def hi_user(username):
    return 'Hello {}!'.format(username)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)

@app.route('/hello/')
@app.route('/hello/<username>')
def hello(username=None):
    return render_template('hello.html', name=username)

with app.test_request_context('/hello', method='GET'):
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='Barry Fang'))
    print(url_for('static', filename='style.css'))
    assert request.path == '/hello'
    assert request.method == 'GET'