# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from typing import Any, Dict

project = "django-revision"
copyright = "2025, Erik van Widenfelt"
author = "Erik van Widenfelt"
release = "1.0.0"
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_inline_tabs",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for intersphinx -------------------------------------------------
#

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# -- Options for extlinks ----------------------------------------------------
#
extlinks = {
    "pypi": ("https://pypi.org/project/%s/", "%s"),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_js_files = []
html_context: Dict[str, Any] = {}

html_theme = "furo"
html_title = "django-revision"
html_static_path = ["_static"]
html_css_files = ["pied-piper-admonition.css"]

html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ]
}

html_theme_options = {
    "source_repository": "https://github.com/erikvw/django-revision",
    "source_branch": "develop",  # or 'develop', 'master', etc.
    "source_directory": "docs/",  # The directory where your RST files live
}
pygments_style = "sphinx"

# EPUB options
epub_show_urls = "footnote"

html_css_files += [
    "https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css",
    "https://assets.readthedocs.org/static/css/badge_only.css",
]
html_js_files += [
    "readthedocs-dummy.js",
    "https://assets.readthedocs.org/static/javascript/readthedocs-doc-embed.js",
]

html_context["current_version"] = "latest"
html_context["display_github"] = True
html_context["github_user"] = "erikvw"
html_context["github_repo"] = "django-revision"
html_context["github_version"] = "develop"
# html_context["conf_py_path"] = ""
html_context["slug"] = "django-revision"


html_css_files += [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]

html_theme_options: Dict[str, Any] = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/erikvw/django-revision/",
            "html": """
                    <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                    </svg>
                """,  # noqa
            "class": "",
        },
    ],
    "source_repository": "https://github.com/erikvw/django-revision/",
    "source_branch": "develop",
    "source_directory": "docs",
}
