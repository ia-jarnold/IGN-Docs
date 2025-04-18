from flask import Flask
from flask import send_from_directory
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
import json

LOG_PATH = './logs'
DOCS_DIR = './docs'

BUILD_LOG = LOG_PATH + '/build.log'
BUILD_DIR = DOCS_DIR + '/build'
RST_SOURCE = DOCS_DIR + '/source' # rst sources before build
SPEC_DIR = RST_SOURCE + '/specs' # rst sources before build
STATIC_DIR = BUILD_DIR + '/html' # docs are built from source to html
SOURCE_DIR = STATIC_DIR + '/_sources' # these are rst sources after build
ARCHIVE_DIR = './tmp'

DATE_FMT = "%m/%d/%Y %H:%M:%S"

app = Flask(__name__, static_url_path='/', static_folder=STATIC_DIR)
app.config['PROPAGATE_EXCEPTIONS'] = False # not sure yet...this was mentioned off hand with the below log combo.


# not always the best but easy way to get all logs in 1 place...
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

gunicorn_logger.info('Starting Flask Server')

def _clean_directory(dir_path):

    gunicorn_logger.info('cleaning docs %s' % dir_path)

    for root, dirs, files in os.walk(dir_path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def _get_referer(request):
    referer = request.headers['referer']
    comps = urllib.parse.urlparse(referer)
    referer = comps.path

# will rebuild docs from source (docs/source -> docs/build/html)
# cleans old docs dir for full rebuild
def build_docs():

    now = datetime.now().strftime(DATE_FMT)

    _clean_directory(BUILD_DIR + '/html/')
    _clean_directory(BUILD_DIR + '/doctrees/')

    with open(BUILD_LOG, 'w') as build_log:
        p = subprocess.run(['make','html'], cwd = DOCS_DIR, stdout=build_log, stderr=build_log)
        build_log.write('Finished ' + now + '\n')

def archive_docs(): # create a tarball of docs html/js/css etc...ARCHIVE_DIR.

    p = subprocess.run(['tar', '-czvf', (ARCHIVE_DIR + '/docs.tar.gz'), STATIC_DIR], cwd = '.')

# this will extend so that other actions return us to the original page eventually
def read_source(request):

    # referer is like the browser page/url that made source api call....
    # however some won't map 1-1 like /docs -> index...
    referer = request.headers['referer']
    comps = urllib.parse.urlparse(referer)
    referer = comps.path

    gunicorn_logger.info('Viewing source file for %s' % referer)

    if  referer == '/docs' or referer == '/': # special cases

        return ('','index.rst.txt')

    else: # most derived cases...html path/referrer close to file path

        # break up referer(url that sent this request)url
        comps = referer.split('/') 
        # get source file for replace end of path...
        srcf = comps[-1].replace('.html','.rst.txt')
        # get source path to update send_from_dir SOURCE_DIR with full path 
        srcfp = '/'.join(comps[:-1])
        return (srcfp, srcf)

def update_links(request):

    id = request.args.get('id')
    link = request.args.get('link')
    remove_link = request.args.get('remove_link')

    gunicorn_logger.info('Managing %s : %s' % (id, link))
    gunicorn_logger.info('Remove %s' % str(remove_link))
    # Beware here be user sting input................................
    if id is None or \
       id == "" or \
       ((link is None or link == "") and remove_link is None):

        gunicorn_logger.info('No link info provided')
        return

    # more sanitation... we know we have somthing...
    id = str(id).strip()
    link = str(link).strip()

    # start process
    with open('%s/links.json' % (SPEC_DIR), 'r') as f:
        links_json = json.load(f)
   
    # sort links by id

    if remove_link is not None: # may need to cast
        del links_json[id]
    else:
        # otherwise add/update the link
        links_json[id] = link

    links_json = { k: links_json[k] for k in sorted(links_json) }

    # refresh json...spec
    gunicorn_logger.info(str("%s") % links_json)
    with open('%s/links.json' % (SPEC_DIR), 'w') as f:
         json.dump(links_json, f)
    
    # loop through json and build links.rst in mem then write one time sphinx uses this to populate links
    links_rst = "" # text...
    for link_id in links_json:
        links_rst += ".. _%s: %s\n" % (link_id, links_json[link_id])

    # write array lines to buffer.
    gunicorn_logger.info(str("%s") % links_rst)
    with open('%s/links.rst' % (RST_SOURCE), 'w') as f:
        f.write(links_rst)

# ROUTES
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

    # build a new archive and serve.
    return send_from_directory(ARCHIVE_DIR, 'docs.tar.gz', as_attachment=True)

@app.route("/ulink")
def ulink():
   
    gunicorn_logger.info('Adding/updating link') 
    update_links(request)

    gunicorn_logger.info('Rebuilding Docs') 
    build_docs()

    # build a new archive and serve.
    return redirect(url_for('index'))

# build initial docs on server load if no index is there. for dev atm really
if not os.path.isfile(STATIC_DIR + '/index.html'):
    gunicorn_logger.info('Running an initial build')
    build_docs()

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
