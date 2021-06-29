# Copyright (C) 2021
# Author: Kacper Sokol <ks1591@my.bristol.ac.uk>
# License: new BSD
"""
Implements the `cssterm` directive for Jupyter Book and Sphinx.
"""

import os
import sys

from docutils import nodes
from docutils.parsers.rst import Directive

import sphinx_term

DEPENDENCIES = {  # See sphinx_term/_static/README.md for more info
    # jQuery (MIT): https://github.com/jquery/jquery
    'jquery.js': 'https://code.jquery.com/jquery-latest.min.js'
}

STATIC_CSS_FILES = ['cssterm/css/cssterm.css']
STATIC_JS_FILES = ['cssterm/scripts/cssterm.js']
STATIC_FILES = STATIC_CSS_FILES + STATIC_JS_FILES

REFNAME = 'terminal box'

if sys.version_info >= (3, 0):
    unicode = str


#### cssterm directive ########################################################


class cssterm_anchor(nodes.General, nodes.Element):
    """A `docutils` node anchoring cssterm boxes."""


def visit_cssterm_anchor_node(self, node):
    """Builds an opening HTML tag for cssterm anchors."""
    self.body.append(self.starttag(node, 'div'))


def depart_cssterm_anchor_node(self, node):
    """Builds a closing HTML tag for cssterm anchors."""
    self.body.append('</div>\n')


def visit_cssterm_anchor_node_(self, node):
    """Builds a prefix for embedding cssterm anchors in LaTeX and raw text."""
    raise NotImplemented


def depart_cssterm_anchor_node_(self, node):
    """Builds a postfix for embedding cssterm anchors in LaTeX and raw text."""
    raise NotImplemented


class cssterm_box(nodes.literal_block, nodes.Element):
    """A `docutils` node holding cssterm boxes."""


def visit_cssterm_box_node(self, node):
    """Builds an opening HTML tag for cssterm boxes."""
    self.body.append(self.starttag(node, 'div', CLASS='cssterm'))


def depart_cssterm_box_node(self, node):
    """Builds a closing HTML tag for cssterm boxes."""
    self.body.append('</div>\n')


def visit_cssterm_box_node_(self, node):
    """Builds a prefix for embedding cssterm boxes in LaTeX and raw text."""
    raise NotImplemented


def depart_cssterm_box_node_(self, node):
    """Builds a postfix for embedding cssterm boxes in LaTeX and raw text. """
    raise NotImplemented


class CSSterm(Directive):
    """
    Defines the `cssterm` directive that builds cssterm boxes.

    The `cssterm` directive is of the form::
       .. cssterm:: cssterm:1.2.3 (required)

    If loaded from an external file, the box id needs to be a terminal
    transcript file name **with** the `cssterm:` prefix and **without**
    the `.log` extension, located in a single directory.
    The directory is given to Sphinx via the `sphinx_term_cssterm_dir`
    config setting.
    If this parameter is not set, terminal box content must be provided
    explicitly.

    This Sphinx extension monitors the terminal transcript files for changes
    and regenerates the content pages that use them if a change is detected.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True
    option_spec = {}

    def run(self):
        """Builds a cssterm box."""
        env = self.state.document.settings.env

        # retrieve the path to the directory holding the code files
        st_term_dir = env.config.sphinx_term_cssterm_dir
        assert isinstance(st_term_dir, str) or st_term_dir is None

        # get the terminal file name for this particular cssterm box
        assert len(self.arguments) == 1, (
            'Just one argument -- terminal block id (possibly encoding the '
            'code file name -- expected')
        term_filename_id = self.arguments[0]
        assert term_filename_id.startswith('cssterm:'), (
            'The terminal box label ({}) must start with the "cssterm:" '
            'prefix.'.format(term_filename_id))
        assert not term_filename_id.endswith('.log'), (
            'The terminal box label ({}) must not end with the ".log" '
            'extension prefix.'.format(term_filename_id))
        # add the .log extension as it is missing
        term_filename = '{}.log'.format(term_filename_id[8:])

        # if the content is given explicitly, use it instead of loading a file
        if self.content:
            contents = '\n'.join(self.content)
        else:
            localised_directory = sphinx_term.localise_term_directory(
                env.srcdir,
                st_term_dir,
                ('sphinx_term_cssterm_dir', 'cssterm box content'))
            # compose the full path to the code file and ensure it exists
            path_localised = os.path.join(localised_directory, term_filename)
            # path_original = os.path.join(st_term_dir, term_filename)
            sphinx_term.file_exists(path_localised)

            # memorise the association between the document (a content source
            # file) and the terminal box -- this is used for watching for
            # terminal file updates
            env.note_dependency(path_localised)

            # read in the terminal file
            with open(path_localised, 'r') as f:
                contents = f.read().strip('\n')

        # create a cssterm node
        box = cssterm_box(contents.strip(), contents,
                          ids=['{}-box'.format(
                              nodes.make_id(term_filename_id))],
                          label=term_filename_id)
        # create anchor
        anchor = cssterm_anchor()
        # assign label and id (`ids=[nodes.make_id(term_filename_id)]`)
        self.options['name'] = term_filename_id
        self.add_name(anchor)

        # insert the terminal box node into the anchor node
        anchor += box

        return [anchor]


def assign_reference_title(app, document):
    """
    Update the labels record of the standard environment to allow referencing
    cssterm boxes.
    """
    # get the standard domain
    domain = app.env.get_domain('std')

    # go through every cssterm box
    for node in document.traverse(cssterm_anchor):
        # every cssterm box must have exactly one name starting with 'cssterm:'
        assert node['names']
        assert len(node['names']) == 1
        node_name = node['names'][0]

        assert node_name.startswith('cssterm:'), (
            'cssterm box ids must start with cssterm:')
        refname = REFNAME

        # every cssterm box has a single id
        assert len(node['ids']) == 1
        node_id = node['ids'][0]

        # get the document name
        docname = app.env.docname

        # every cssterm box should **already** be referenceable without a title
        assert node_name in domain.anonlabels
        assert domain.anonlabels[node_name] == (docname, node_id)

        # allow this cssterm box to be referenced with the default
        # 'terminal box' stub (REFNAME)
        domain.labels[node_name] = (docname, node_id, refname)


#### Extension setup ##########################################################


def include_static_files(app):
    """
    Copies the static files required by this extension.
    (Attached to the `builder-inited` Sphinx event.)
    """
    for file_name in STATIC_FILES:
        file_path = sphinx_term.get_static_path(file_name)
        if file_path not in app.config.html_static_path:
            app.config.html_static_path.append(file_path)


def load_static_files(app, pagename, templatename, context, doctree):
    """Includes cssterm static files only on pages that use the module."""
    # only go through non-empty documents
    if doctree is None:
        return

    # get cssterm boxes
    cssterm_boxes = doctree.traverse(cssterm_box)
    # skip pages without at least one cssterm box
    if not cssterm_boxes:
        return

    # ensure that custom files were included
    for css_file in STATIC_CSS_FILES:
        _css_file = os.path.basename(css_file)
        if not sphinx_term.is_css_registered(app, _css_file):
            app.add_css_file(_css_file)
    for js_file in STATIC_JS_FILES:
        _js_file = os.path.basename(js_file)
        if not sphinx_term.is_js_registered(app, _js_file):
            app.add_js_file(_js_file)

    # add external dependencies
    script_files = [os.path.basename(i) for i in context['script_files']]
    for stub, path in DEPENDENCIES.items():
        if sphinx_term.is_js_registered(app, path) or stub in script_files:
            continue
        app.add_js_file(path)


def setup(app):
    """
    Sets up the Sphinx extension for the `cssterm` directive.
    """
    # register two Sphinx config values used for the extension
    app.add_config_value('sphinx_term_cssterm_dir', None, 'env')

    # register the custom docutils nodes with Sphinx
    app.add_node(
        cssterm_box,
        html=(visit_cssterm_box_node, depart_cssterm_box_node),
        latex=(visit_cssterm_box_node_, depart_cssterm_box_node_),
        text=(visit_cssterm_box_node_, depart_cssterm_box_node_)
    )
    app.add_node(
        cssterm_anchor,
        html=(visit_cssterm_anchor_node, depart_cssterm_anchor_node),
        latex=(visit_cssterm_anchor_node_, depart_cssterm_anchor_node_),
        text=(visit_cssterm_anchor_node_, depart_cssterm_anchor_node_)
    )

    # register the custom role and directives with Sphinx
    app.add_directive('cssterm', CSSterm)

    # connect custom hooks to the Sphinx build process
    app.connect('doctree-read', assign_reference_title)
    # ...ensure the required static files are **copied** into the build
    app.connect('builder-inited', include_static_files)
    # ...ensure that relevant html output pages **load** the static files
    app.connect('html-page-context', load_static_files)

    return {'version': sphinx_term.VERSION}
