from flask import Flask
from flask import send_from_directory
from flask import redirect, url_for
#from flask import request
from datetime import datetime
import subprocess
import os
import os.path
import logging

LOG_PATH = './logs'
DOCS_DIR = './docs'

BUILD_LOG = LOG_PATH + '/build.log'
BUILD_DIR = DOCS_DIR + '/build'
STATIC_DIR = BUILD_DIR + '/html' # docs are built from source to html
ARCHIVE_DIR = './tmp'

DATE_FMT = "%m/%d/%Y %H:%M:%S"

app = Flask(__name__, static_url_path='/', static_folder=STATIC_DIR)

# not always the best but easy way to get all logs in 1 place...
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
#app.config['PROPAGATE_EXCEPTIONS'] = False # not sure yet...

gunicorn_logger.info('Starting Flask Server')


# will rebuild docs from source (docs/source -> docs/build/html)
def build_docs():

    now = datetime.now().strftime(DATE_FMT)
    with open(BUILD_LOG, 'w') as build_log:
        p = subprocess.run(['make','html'], cwd = DOCS_DIR, stdout=build_log)
        build_log.write('Finished ' + now + '\n')

def archive_docs():
    now = datetime.now().strftime(DATE_FMT)
    p = subprocess.run(['tar', '-czvf', ARCHIVE_DIR + '/docs.tar.gz', STATIC_DIR], cwd = '.')

@app.route("/")
@app.route("/docs")
def index():

    return send_from_directory(STATIC_DIR, 'index.html')

@app.route("/refresh")
@app.route('/build')
def refresh():

    gunicorn_logger.info('Refreshing Docs..see build log in %s' % BUILD_LOG)
    build_docs()
    return redirect(url_for('index'))

@app.route("/backup")
@app.route('/archive')
def backup():

    gunicorn_logger.info('Archiving Docs in %s' % ARCHIVE_DIR) 
    archive_docs()
    return redirect(url_for('index'))

# build initial docs on server load if no index is there. for dev atm really
if not os.path.isfile(STATIC_DIR + '/index.html'):
    gunicorn_logger.info('Running an initial build')
    build_docs()

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
