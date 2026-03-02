# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# ---------------------------------------------------------------------------
# Path setup — make the project root importable so autodoc can import modules
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.abspath(".."))

# ---------------------------------------------------------------------------
# Project information
# ---------------------------------------------------------------------------
project = "Parking System"
copyright = "2026, Parking System Contributors"
author = "Parking System Contributors"
release = "2.0"
version = "2.0"

# ---------------------------------------------------------------------------
# General configuration
# ---------------------------------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",       # Pull docstrings from source
    "sphinx.ext.viewcode",      # Add [source] links
    "sphinx.ext.napoleon",      # NumPy / Google docstring styles
    "sphinx.ext.intersphinx",   # Cross-link to Python stdlib docs
    "sphinx.ext.autosummary",   # Auto-generate summary tables
    "sphinx_design",            # Grid, tab, card, and badge directives
]

autosummary_generate = True

# Mock out all GUI/image libraries so autodoc works in headless CI without
# needing to install tkinter, customtkinter, Pillow, or tkcalendar.
autodoc_mock_imports = [
    "tkinter",
    "customtkinter",
    "PIL",
    "tkcalendar",
]

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "member-order": "bysource",
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True

# Suppress nitpick warnings for mocked GUI base classes that can't be resolved.
nitpick_ignore = [
    ("py:class", "customtkinter.CTkFrame"),
    ("py:class", "customtkinter.CTkToplevel"),
    ("py:class", "customtkinter.CTkBaseClass"),
    ("py:class", "customtkinter.CTk"),
]

# intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# ---------------------------------------------------------------------------
# HTML output — Shibuya theme
# ---------------------------------------------------------------------------
html_theme = "shibuya"
html_static_path = ["_static"]

html_title = "Parking System v2.0"
html_short_title = "Parking System"

html_theme_options = {
    "accent_color": "blue",
    "github_url": "https://github.com/paarthsiloiya/Parking-System",
    "nav_links": [
        {"title": "Setup", "url": "setup"},
        {"title": "Usage", "url": "usage"},
        {"title": "Architecture", "url": "architecture"},
        {"title": "API Reference", "url": "api/index"},
    ],
}

html_copy_source = False
