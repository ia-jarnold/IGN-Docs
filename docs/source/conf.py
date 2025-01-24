# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'IGN-Docs'
copyright = '2024, Jared Arnold'
author = 'Jared Arnold'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = ['sphinx_design']

templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'links.rst']

# make rst_epilog a variable, so you can add other epilog parts to it
rst_epilog =""
# Read link all targets from file
with open('links.rst') as f:
    rst_epilog += f.read()

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_nefertiti'
html_static_path = ['_static', '_static/html']

# Starting doc roots...jinja variables
years = ['2021', '2022', '2023']
ign_versions = ['8.1.44']
ign_tickets  = ['137089']
ign_subsystem = ['OPC-UA']

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

html_context = { # makes varaiables accessable in jinja
    'years' : years,
    'ign_versions': ign_versions,
    'ign_subsystem': ign_subsystem,
    'ign_tickets': ign_tickets
}
