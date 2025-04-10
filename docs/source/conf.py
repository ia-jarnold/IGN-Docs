# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# ANY PRINT STATEMENTS IN HERE WILL SHOW UP IN THE PACKAGE_ROOT/logs/build_log
import json
from os import listdir
from os.path import isfile, join

project = 'IGN-Docs'
copyright = '2025, Jared Arnold'
author = 'Jared Arnold'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [ 'sphinx_design',  # add dropdowns/cards/grids...
               'sphinx_favicon', # adds a favicon
               'myst_parser', # add markdown support
               'sphinx.ext.autosectionlabel', # Internal links(H1/H2/H3)
               'sphinx.ext.extlinks' # helps template external links link ign java docs
             ] # ass :ref:`` header links

templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'links.rst', 's5defs.rst']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
#html_theme = 'sphinx_nefertiti'
html_theme = 'classic' # good for testing against actual theme

html_static_path = ['_static', '_static/html', '_static/images']

#https://sphinx-design.readthedocs.io/en/latest/badges_buttons.html
html_css_files = [
    #'css/nefertiti_ext.css',
    'css/text_colors.css',
    'css/classic_ext.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css'
]

favicons = [
    'ignition_fav.png'
]

rst_epilog =""
# Read link all targets from file
with open('links.rst') as f:
    rst_epilog += f.read()

with open('s5defs.rst') as f:
     rst_epilog += f.read()

# allow templating of rst files using configurations
# https://ericholscher.com/blog/2016/jul/25/integrating-jinja-rst-sphinx/
def rstjinja(app, docname, source):
   """
   Render our pages as a jinja template for fancy templating goodness.
   """
   # Make sure we're outputting HTML
   if app.builder.format != 'html':
       return
   src = source[0]
   rendered = app.builder.templates.render_string(
       src, app.config.html_context
   )
   source[0] = rendered

def setup(app):
   app.connect("source-read", rstjinja)

# Build specs and put them in html_context for jijna also
# if editing spec directly hidden .swp files can sneak in so beware...will fail build
SPEC_PATH = './specs'
SPECS = [f[:-5] for f in listdir(SPEC_PATH) if isfile(join(SPEC_PATH, f))]
spec_data = {}
for spec in SPECS:

  print(spec)
  with open('%s/%s.json' % (SPEC_PATH, spec), 'r') as f:
      spec_data[spec] = json.load(f)

years             = spec_data['years'] 
links             = spec_data['links']
ign_versions      = spec_data['ign_versions'] 
ign_tickets       = spec_data['ign_tickets']
ign_loggers       = sorted([ign_log.lower() for ign_log in spec_data['ign_loggers']])
ign_subsystem     = spec_data['ign_subsystem']
links             = spec_data['links']
test              = [1,2,3,4,5,6]

html_context = { # makes varaiables accessable in jinja
    'years' :        years,
    'ign_versions':  ign_versions,
    'ign_subsystem': ign_subsystem,
    'ign_tickets':   ign_tickets,
    'ign_loggers':   ign_loggers,
    'links'  :links,
    'test'  :test
}

extlinks = {
  'ign_java_doc_8.1' : ('https://files.inductiveautomation.com/sdk/javadoc/ignition81/%s/index.html', '%s IGN Java docs' )
}
