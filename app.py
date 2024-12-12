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

#@app.route('/print')
#def print():
#
#    with open(LOG_PATH + '/gunicorn.log', 'w') as g_log: 
#        p = subprocess.run(['gunicorn','--help'], cwd = '.', stdout=g_log)
#
#    # will rebuild docs from source (docs/source)
#    return redirect(url_for('index'))

if __name__ == "__main__":

    # rebuild docs if servce restarts doing so in the Docker on image create file will
    # remove this build when volums are connected since we have no local
    # build and want to have the dev directory exposed atm...if we move the dev directory
    # valume back down to only docs source image can hold initial build. But right now I am 
    # looking at everything.
    p = subprocess.run(['make','html'], cwd = DOCS_DIR, stdout=build_log)
    app.run(host="0.0.0.0", port=5000)

