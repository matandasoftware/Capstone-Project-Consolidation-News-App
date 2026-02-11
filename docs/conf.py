# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

# -- Django Configuration ---------------------------------------------------
import os
import sys
import django

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath('..'))

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_project.settings'

# Initialize Django
django.setup()
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'News Application'
copyright = '2026, Mudau Pfarelo Channel'
author = 'Mudau Pfarelo Channel'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Automatically document from docstrings
    'sphinx.ext.viewcode',     # Add links to source code
    'sphinx.ext.napoleon',     # Support Google/NumPy docstring styles
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

