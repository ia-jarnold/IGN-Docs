from flask import Flask
from flask import send_from_directory
from flask import redirect, url_for
import subprocess
import os

LOG_PATH = './logs'
DOCS_DIR = './docs'

BUILD_LOG = LOG_PATH + '/build.log'
BUILD_DIR = DOCS_DIR + '/build'
STATIC_DIR = BUILD_DIR + '/html' # docs are  built from source to html

app = Flask(__name__, static_url_path='/', static_folder=STATIC_DIR)

# https://dev.to/rtficial/serving-static-files-and-creating-websites-using-python-flask-41c3
@app.route("/")
@app.route("/docs")
def index():
    return send_from_directory('./docs/build/html', 'index.html') 

@app.route("/refresh")
@app.route('/build')
def refresh():

    with open(BUILD_LOG, 'w') as build_log: 
        p = subprocess.run(['make','html'], cwd = DOCS_DIR, stdout=build_log)

    # will rebuild docs from source (docs/source)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
