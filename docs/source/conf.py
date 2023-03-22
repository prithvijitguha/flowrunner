# -*- coding: utf-8 -*-
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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "flowrunner"
copyright = "2023, Prithvijit Guha"
author = "Prithvijit Guha"

# The full version, including alpha/beta/rc tags
release = "2023"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinxcontrib.mermaid", "sphinx_tabs.tabs", "autoapi.extension"]

# Sphinx autoapi related
autoapi_type = 'python'
autoapi_dirs = ['../../flowrunner', '../../examples']

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# Required theme setup
html_theme = "sphinx_material"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# Set link name generated in the top bar.
html_title = "flowrunner"

# Material theme options (see theme.conf for more information)
html_theme_options = {
    # Set the name of the project to appear in the navigation.
    "nav_title": "flowrunner",
    # Set you GA account ID to enable tracking
    "google_analytics_account": "UA-XXXXX",
    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    "base_url": "https://github.com/prithvijitguha/flowrunner",
    # Set the color and the accent color
    "color_primary": "indigo",
    "color_accent": "orange",
    # Set the repo location to get a badge with stats
    "repo_url": "https://github.com/prithvijitguha/flowrunner",
    "repo_name": "flowrunner",
    # Visible levels of the global TOC; -1 means unlimited
    "globaltoc_depth": 1,
    # If False, expand all TOC entries
    "globaltoc_collapse": False,
    # If True, show hidden TOC entries
    "globaltoc_includehidden": False,
}

html_sidebars = {"**": ["globaltoc.html"]}
