from flask import Flask
from flask import send_from_directory
from flask import redirect
from flask import url_for
from flask import request

from datetime import datetime
import subprocess
import os
import os.path
import logging
import shutil
import urllib.parse
import json

# Logs
LOG_PATH    = './logs'
BUILD_LOG   = LOG_PATH + '/build.log'

# Docs
DOCS_DIR    = './docs'
BUILD_DIR   = DOCS_DIR + '/build'
RST_SOURCE  = DOCS_DIR + '/source' # rst sources before build
SPEC_DIR    = RST_SOURCE + '/specs' # json sources before build
STATIC_DIR  = BUILD_DIR + '/html' # docs are built from rst_source to html
SOURCE_DIR  = STATIC_DIR + '/_sources' # these are rst sources after in html build(what is archived)

# Archive
ARCHIVE_DIR = './tmp' # archive dir.

DATE_FMT = "%m/%d/%Y %H:%M:%S" # common date format

app = Flask(__name__, static_url_path='/', static_folder=STATIC_DIR)
app.config['PROPAGATE_EXCEPTIONS'] = False # not sure yet...this was mentioned off hand with the below log pipe combo.

# not always the best but easy way to get all logs in 1 place...
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

gunicorn_logger.info('Starting Flask Server')

def _clean_directory(dir_path):

    gunicorn_logger.info('cleaning directory %s' % dir_path)

    for root, dirs, files in os.walk(dir_path):

        for f in files:

            os.unlink(os.path.join(root, f))

        for d in dirs:

            shutil.rmtree(os.path.join(root, d))

def _manage_links_spec(id, link, remove_link): # lots of CRUD ops in 1...for now....
    
    gunicorn_logger.info('updating links spec')

    with open('%s/links.json' % (SPEC_DIR), 'r') as f: # READ
        links_json = json.load(f)
 
    if remove_link is not None: # may need to cast # DELETE
        del links_json[id]
    else:
        # otherwise add/update the link # UPDATE/INSERT
        links_json[id] = link
   
    # sort the json links. # SORT
    links_json = { k: links_json[k] for k in sorted(links_json) }

    # refresh json...spec # WRITE
    gunicorn_logger.info(str("%s") % links_json)
    with open('%s/links.json' % (SPEC_DIR), 'w') as f:
         json.dump(links_json, f)

    return links_json # updated links spec

def _get_referer(request): # returns referer as path.../docs, /Links/links_view

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

        p = subprocess.run( ['make','html'], cwd = DOCS_DIR, stdout=build_log, stderr=build_log )
        build_log.write('Finished ' + now + '\n')

def archive_docs(): # create a tarball of docs html/js/css etc...ARCHIVE_DIR.

    p = subprocess.run(['tar', '-czvf', (ARCHIVE_DIR + '/docs.tar.gz'), STATIC_DIR], cwd = '.')

# this action returns original page source
# some sphinx themes have this by default like classic(current) on side bar
# but useful
def read_source(request):

    # referer is like the browser page/url that made source api call....
    # however some won't map 1-1 like /docs -> index.html...
    referer = _get_referer(request)

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

def refresh_links(request): # Action(request) based

    # process request
    id          = request.args.get('id')
    link        = request.args.get('link')
    remove_link = request.args.get('remove_link') # None or a value I believe

    gunicorn_logger.info('Managing %s : %s Remove? %s' % (id, link, remove_link))

    # Check User input params/query params/body....all entered by user/process
    # Beware here be user sting input................................
    if id is None or \
       id == "" or \
       ((link is None or link == "") and remove_link is None):

        gunicorn_logger.info('No link info provided')
        return

    # more sanitation... we know we have somthing...
    id   = str(id).strip()
    link = str(link).strip()

    links_json = _manage_links_spec(id, link, remove_link) # update links spec
    
    # loop through sorted/updated json spec and build links.rst
    # in mem then write one time sphinx uses this to populate links
    links_rst = "" # text...
    for link_id in links_json:

        # .. _LINK_ID1: LINK_URL1\n
        # .. _LINK_ID2: LINK_URL2\n
        # ....
        links_rst += ".. _%s: %s\n" % (link_id, links_json[link_id])

    # write array lines to .rst file
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
    refresh_links(request)

    gunicorn_logger.info('Rebuilding Docs') 
    build_docs()

    # build a new archive and serve.
    return redirect(url_for('index'))

# build initial docs on server load if no index is there. for dev atm really
if not os.path.isfile( STATIC_DIR + '/index.html' ):
    gunicorn_logger.info('Running an initial build')
    build_docs()

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
