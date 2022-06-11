# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import logging
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))
sys.path.append(os.path.abspath('extensions'))


# -- Project information -----------------------------------------------------

project = "Arya's API Framework"
copyright = '2022, Aryathel'
author = 'Aryathel'
version = "0.1.4"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'builder',
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_paramlinks',
    'sphinxcontrib_trio',
    'details',
    'exception_hierarchy',
    'attributetable',
    'resourcelinks',
    'nitpick_file_ignorer'
]

# Autodoc settings
autodoc_member_order = 'bysource'
autodoc_typehints = 'none'

# Intersphinx links
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# External links
extlinks = {
    'pydantic': ('https://pydantic-docs.helpmanual.io/%s', '%s'),
}

# Napoleon settings
napoleon_numpy_docstring = True
napoleon_use_rtype = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

source_suffix = '.rst'
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_experimental_html5_writer = True
html_theme = 'basic'

pygments_style = 'friendly'

resource_links = {
    'aiohttp': 'https://docs.aiohttp.org/en/stable/',
    'requests': 'https://requests.readthedocs.io/en/latest/',
    'pydantic': 'https://pydantic-docs.helpmanual.io/',
    'postmanecho': 'https://www.postman-echo.com/',
}

rst_prolog = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |maybecoro| replace:: This function *could be a* |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine
.. |deco| replace:: This function is a decorator*.
"""

# This is really hacky, but this allows me to do some stuff by
# adding "|inherited|" to the end of a docstring to make it appear
# with the "(inherited)" qualifier in an attribute table.
rst_epilog = """
.. role:: raw-html(raw)
    :format: html

.. |inherited| replace:: :raw-html:`<div style="display: none;" hidden></div>`
"""

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['static']

html_logo = os.path.abspath('static/logo_125x.png')
html_favicon = os.path.abspath('static/logo.png')

html_search_scorer = os.path.abspath('static/scorer.js')
html_js_files = [
    'custom.js',
    'settings.js',
    'copy.js',
    'sidebar.js'
]

html_show_sourcelink = False

github_url = "https://github.com/Aryathel/APIFramework"

# Theme config
html_theme_options = {
}


def _i18n_warning_filter(record: logging.LogRecord) -> bool:
  return not record.msg.startswith(
    (
      'inconsistent references in translated message',
      'inconsistent term references in translated message',
    )
  )


_i18n_logger = logging.getLogger('sphinx')
_i18n_logger.addFilter(_i18n_warning_filter)
