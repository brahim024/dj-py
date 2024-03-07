# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import datetime
import pathlib
import sys

import toml

ROOT_DIR = pathlib.Path(__file__).parents[2].resolve()
sys.path.append(ROOT_DIR.as_posix())

pyproject = toml.load((ROOT_DIR / "pyproject.toml").as_posix())
poetry = pyproject["tool"]["poetry"]

project = poetry["name"]
copyright = f"{datetime.datetime.now().year}, Brahim024"
author = poetry["authors"][0]
release = version = poetry["version"]

# -- Project information -----------------------------------------------------


project = 'djpay'
copyright = '2024, brahim'
author = 'brahim'
release = '0.2.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    'preamble': '',

    # Latex figure (float) alignment

    'figure_align': 'htbp'
}

