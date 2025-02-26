from flask import Flask
from flask import send_from_directory
from flask import redirect, url_for
from flask import request
from datetime import datetime
import subprocess
import os
import os.path
import logging
import shutil
import urllib.parse

LOG_PATH = './logs'
DOCS_DIR = './docs'

BUILD_LOG = LOG_PATH + '/build.log'
BUILD_DIR = DOCS_DIR + '/build'
STATIC_DIR = BUILD_DIR + '/html' # docs are built from source to html
SOURCE_DIR = STATIC_DIR + '/_sources'
ARCHIVE_DIR = './tmp'

DATE_FMT = "%m/%d/%Y %H:%M:%S"

app = Flask(__name__, static_url_path='/', static_folder=STATIC_DIR)

# not always the best but easy way to get all logs in 1 place...
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
app.config['PROPAGATE_EXCEPTIONS'] = False # not sure yet...

gunicorn_logger.info('Starting Flask Server')

def _clean_directory(dir_path):

    gunicorn_logger.info('cleaning docs %s' % dir_path)

    for root, dirs, files in os.walk(dir_path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

# will rebuild docs from source (docs/source -> docs/build/html)
# cleans old docs dir for full rebuild
def build_docs():

    now = datetime.now().strftime(DATE_FMT)

    _clean_directory(BUILD_DIR + '/html/')
    _clean_directory(BUILD_DIR + '/doctrees/')

    with open(BUILD_LOG, 'w') as build_log:
        p = subprocess.run(['make','html'], cwd = DOCS_DIR, stdout=build_log, stderr=build_log)
        build_log.write('Finished ' + now + '\n')

def archive_docs(): # create a tarball of docs html/js/css etc...in tmp

    p = subprocess.run(['tar', '-czvf', (ARCHIVE_DIR + '/docs.tar.gz'), STATIC_DIR], cwd = '.')

# this will extend so that other actions return us to the original page eventually
def read_source(request):

    # referer is like the browser page/url that made source api call....
    # however some won't map 1-1 like /docs -> index...
    referer = request.headers['referer']

    gunicorn_logger.info('Viewing ource file for %s' % referer)

    comps = urllib.parse.urlparse(referer)
    referer = comps.path

    if  referer == '/docs' or referer == '/':

        return ('','index.rst.txt')

    else:

        # break up referer(url that sent this request)url
        comps = referer.split('/') 
        # get source file for replace end of path...
        srcf = comps[-1].replace('.html','.rst.txt')
        # get source path to update send_from_dir SOURCE_DIR with full path 
        srcfp = '/'.join(comps[:-1])
        return (srcfp, srcf)


@app.route("/")
@app.route("/docs")
def index():

    return send_from_directory(STATIC_DIR, 'index.html')

@app.route("/source")
def source():
  
    (srcfp, srcf) = read_source(request)
    return send_from_directory(SOURCE_DIR + '/%s' % srcfp, srcf)

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
