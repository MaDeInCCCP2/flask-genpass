from flask import Flask, render_template, request, redirect, url_for, flash
import random
import string

app = Flask(__name__)

def gen_passwordeasy():
    chars = list(string.ascii_uppercase + string.ascii_lowercase)
    res = random.sample(chars, 5)
    return ''.join(res)


def gen_passwordmedium():
    chars = list(string.ascii_uppercase + string.ascii_lowercase + string.digits)
    res = random.sample(chars, 10)
    return ''.join(res)

def gen_passwordhard():
    chars = list(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation)
    res = random.sample(chars, 16)
    return ''.join(res)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generateeasy', methods=['GET'])
def generate_easy():
    password = gen_passwordeasy()
    return render_template('index.html', password=password)

@app.route('/generatemedium', methods=['GET'])
def generate_medium():
    password = gen_passwordmedium()
    return render_template('index.html', password=password)

@app.route('/generatehard', methods=['GET'])
def generate_hard():
    password = gen_passwordhard()
    return render_template('index.html', password=password)

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, host='0.0.0.0', port=5000, )