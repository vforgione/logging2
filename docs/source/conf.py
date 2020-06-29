#!/usr/bin/env python3

import codecs
import os
import re
import sys


sys.path.insert(0, os.path.abspath("../../logging2"))


# -- General configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_annotation",
]

templates_path = ["_templates"]

source_suffix = ".rst"

master_doc = "index"

project = "logging2"
copyright = "2017, Vince Forgione"
author = "Vince Forgione"

_setuppy = codecs.open(os.path.abspath("../../setup.py"), encoding="utf8").read()
_version = re.search("^VERSION = [\"']([^\"']+)[\"']", _setuppy, re.MULTILINE).group(1)
version = release = _version

language = None

exclude_patterns = []

pygments_style = "sphinx"

todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

html_theme = "alabaster"

# html_theme_options = {}

html_static_path = ["_static"]


# -- Options for HTMLHelp output ------------------------------------------

htmlhelp_basename = "logging2doc"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {}

latex_documents = [
    (master_doc, "logging2.tex", "logging2 Documentation", "Vince Forgione", "manual"),
]


# -- Options for manual page output ---------------------------------------

man_pages = [(master_doc, "logging2", "logging2 Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (
        master_doc,
        "logging2",
        "logging2 Documentation",
        author,
        "logging2",
        "One line description of project.",
        "Miscellaneous",
    ),
]
