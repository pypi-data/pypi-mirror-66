# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
import sys
sys.path.insert(0, "/home/henrikj/Documents/polyfemos_1/polyfemos_SOURCE/polyfemos")
# sys.path.insert(0, "/home/henrik/Documents/polyfemos/polyfemos_DEV/code/front")
# sys.path.insert(0, "/home/henrik/Documents/polyfemos/polyfemos_DEV/code/back")
# sys.path.insert(0, os.path.abspath('..'))
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'polyfemos'
copyright = '2019, University of Oulu'
author = 'HJ'


# The short X.Y version
version = '0.0.0'
# The full version, including alpha/beta/rc tags
release = ''

versionfile = "/home/henrikj/Documents/polyfemos_1/polyfemos_SOURCE/polyfemos/VERSION.txt"
with open(versionfile, 'r') as f:
    version = f.readline().strip()
release = version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosummary',
    'sphinxcontrib.autohttp.flask',
    'sphinxcontrib.autohttp.flaskqref',
    # 'sphinx_autodoc_typehints',
    # 'jinja2.ext.do',
    # 'autosummary',
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# always_document_param_types = True

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
# source_suffix = '.rst'

# The master toctree document.
master_doc = 'documentation_index'


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
]

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'classic'
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    # 'bgcolor':'#000000'
    'page_width': '80%',

    # Tab name for entire site. (Default: "Site")
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_show_sourcelink = True


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'polyfemosdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'polyfemos.tex', 'polyfemos Documentation',
     'HJ', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'polyfemos', 'polyfemos Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'polyfemos', 'polyfemos Documentation',
     author, 'polyfemos', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
# intersphinx_mapping = {'https://docs.python.org/': None}
# objects.inv should be found in these locations
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.7', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'flask': ('http://flask.palletsprojects.com/en/1.1.x/', None),
    'flask_wtf': ('https://flask-wtf.readthedocs.io/en/stable/', None),
    'obspy': ('https://docs.obspy.org/', None),
    'bokeh': ('https://bokeh.pydata.org/en/latest/', None),
    'pathos': ('https://pathos.readthedocs.io/en/latest/', None),
    'PIL': ('https://pillow.readthedocs.io/en/stable/', None),
    'matplotlib': ('https://matplotlib.org/', None),
    'werkzeug': ('https://werkzeug.palletsprojects.com/en/0.15.x/', None),
    'sklearn': ('https://scikit-learn.org/stable/', None),
}

# add_module_names = False

autosummary_generate = True
# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
# todo_include_todos = True

# autodoc_member_order = 'groupwise'
# autoclass_content = 'class'
# nitpicky = True

# def setup(app):
#     app.add_stylesheet('custom.css')

# highlight_language = 'none'

# warn about *all* references where the target cannot be found
# nitpicky = True
