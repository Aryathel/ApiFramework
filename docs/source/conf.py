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
import re

sys.path.insert(0, os.path.abspath('../../'))
sys.path.append(os.path.abspath('extensions'))

# -- Project information -----------------------------------------------------

project = None
with open('../../arya_api_framework/__init__.py') as f:
    project = re.search(r'^__project__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    if not project:
        raise RuntimeError('__project__ is not set.')
copyright = None
with open('../../arya_api_framework/__init__.py') as f:
    copyright = re.search(r'^__copyright__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    if not copyright:
        raise RuntimeError('__copyright__ is not set.')
author = None
with open('../../arya_api_framework/__init__.py') as f:
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    if not author:
        raise RuntimeError('__author__ is not set.')
version = None
with open('../../arya_api_framework/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    if not version:
        raise RuntimeError('__version__ is not set.')

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
    'sphinx_toolbox.shields',
    'details',
    'exception_hierarchy',
    'attributetable',
    'resourcelinks',
    'nitpick_file_ignorer',
    'checklist'
]

# Autodoc settings
autodoc_member_order = 'bysource'
autodoc_typehints = 'none'

# Intersphinx links
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://requests.readthedocs.io/en/stable/', None),
    'aiohttp': ('https://docs.aiohttp.org/en/stable/', None),
}

# External links
extlinks = {
    'pydantic': ('https://pydantic-docs.helpmanual.io/%s', '%s'),
    'http': ('https://www.rfc-editor.org/rfc/rfc9110.html#%s', '%s')
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
html_experimental_html5_writer = True
html_theme = 'basic'

pygments_style = 'friendly'

resource_links = {
    'aiohttp': 'https://docs.aiohttp.org/en/stable/',
    'requests': 'https://requests.readthedocs.io/en/latest/',
    'pydantic': 'https://pydantic-docs.helpmanual.io/',
    'ratelimit': 'https://pypi.org/project/ratelimit/'
}

rst_prolog = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |maybecoro| replace:: This function *could be a* |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine

.. |deco| replace:: This function is a decorator.

.. |validated_method| replace:: This method enforces |data_validation|_.
.. |validated_class| replace:: This class enforces |data_validation|_.
.. |data_validation| replace:: *data validation*
.. _data_validation: https://pydantic-docs.helpmanual.io/usage/validation_decorator/

.. |sync_rate_limited_method| replace:: This method *can* enforce |sync_rate_limit|_.
.. |async_rate_limited_method| replace:: This method *can* enforce |async_rate_limit|_.
.. |sync_rate_limit| replace:: *rate limits*
.. _sync_rate_limit: https://github.com/tomasbasham/ratelimit
.. |async_rate_limit| replace:: *rate limits*
.. _async_rate_limit: https://aiolimiter.readthedocs.io/en/latest/

.. |readonly| replace:: *This is a read-only attribute.*
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

# Toolbox options
github_username = "Aryathel"
github_repository = "ApiFramework"


def _i18n_warning_filter(record: logging.LogRecord) -> bool:
    return not record.msg.startswith(
        (
            'inconsistent references in translated message',
            'inconsistent term references in translated message',
        )
    )


_i18n_logger = logging.getLogger('sphinx')
_i18n_logger.addFilter(_i18n_warning_filter)
