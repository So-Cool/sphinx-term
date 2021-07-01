# Copyright (C) 2021
# Author: Kacper Sokol <ks1591@my.bristol.ac.uk>
# License: new BSD
"""
Implements the `termynal` directive for Jupyter Book and Sphinx.
"""

import os
import sys
import yaml

from docutils import nodes
from docutils.parsers.rst import Directive, directives

import sphinx_term

DEPENDENCIES = {  # See sphinx_term/_static/README.md for more info
}
STYLES = {
    # FiraMono font: https://fonts.google.com/specimen/Fira+Mono
    'firamono.css': 'https://fonts.googleapis.com/css?family=Fira+Mono'
}

STATIC_CSS_FILES = ['termynal/termynal.css']
STATIC_JS_FILES = ['termynal/termynal.js']
STATIC_FILES = STATIC_CSS_FILES + STATIC_JS_FILES

REFNAME = 'terminal box'

TERMYNAL_ATTRS = [
    'prefix',
    'startDelay',
    'typeDelay',
    'lineDelay',
    'progressLength',
    'progressChar',
    'cursor',
    'noInit',
    'lineData'
]
TERMYNAL_LINE_ATTRS = [
    'prompt',
    'progressPercent',
    'progressChar',
    'typeDelay',
    'cursor'
]

if sys.version_info >= (3, 0):
    unicode = str


#### termynal directive #######################################################


class termynal_box(nodes.literal_block, nodes.Element):
    """A `docutils` node holding termynal boxes."""


def visit_termynal_box_node(self, node):
    """Builds an opening HTML tag for termynal boxes."""
    attributes = {'data-termynal': ''}

    for i in TERMYNAL_ATTRS:
        attr = 'data-ty-{}'.format(i.lower())
        attr_text = node.attributes.get(attr, None)
        if attr_text is not None:
            attributes[attr] = attr_text

    self.body.append(self.starttag(node, 'div', **attributes))


def depart_termynal_box_node(self, node):
    """Builds a closing HTML tag for termynal boxes."""
    self.body.append('\n</div>\n')


def visit_termynal_box_node_(self, node):
    """Builds a prefix for embedding termynal boxes in LaTeX and raw text."""
    raise NotImplemented


def depart_termynal_box_node_(self, node):
    """Builds a postfix for embedding termynal boxes in LaTeX and raw text. """
    raise NotImplemented


class termynal_line(nodes.literal_block, nodes.Element):
    """A `docutils` node holding termynal lines."""


def visit_termynal_line_node(self, node):
    """Builds an opening HTML tag for termynal lines."""
    attributes = {'data-ty': node.attributes.get('type', '')}

    for i in TERMYNAL_LINE_ATTRS:
        i_low = i.lower()
        attr = 'data-ty-{}'.format(i_low)
        attr_text = node.attributes.get(i_low, None)
        if attr_text is not None:
            attributes[attr] = attr_text

    self.body.append(self.starttag(node, 'span', suffix='', **attributes))


def depart_termynal_line_node(self, node):
    """Builds a closing HTML tag for termynal lines."""
    self.body.append('</span>\n')


def visit_termynal_line_node_(self, node):
    """Builds a prefix for embedding termynal lines in LaTeX and raw text."""
    raise NotImplemented


def depart_termynal_line_node_(self, node):
    """Builds a postfix for embedding termynal lines in LaTeX and raw text. """
    raise NotImplemented


class Termynal(Directive):
    """
    Defines the `termynal` directive that builds termynal boxes.

    The `termynal` directive is of the form::
       .. termynal:: termynal:1.2.3 (required)

    If loaded from an external file, the box id needs to be a terminal
    transcript file name **with** the `termynal:` prefix and **without**
    the `.yml` extension, located in a single directory.
    The directory is given to Sphinx via the `sphinx_term_termynal_dir`
    config setting.
    If this parameter is not set, terminal box content must be provided
    explicitly.

    The `termynal` directive takes a number of configuration parameters,
    which correspond to the underlying `termynal HTML configuration`_:

    prefix
      Prefix to use for data attributes. `ty` by default.
    startDelay
      Delay before animation given in milliseconds. `600` by default.
    typeDelay
      Delay between each typed character given in milliseconds.
      `90` by default.
    lineDelay
      Delay between each line given in milliseconds. `1500` by default.
    progressLength
      Number of characters displayed as progress bar. `40` by default.
    progressChar
      Character used for progress bar. `█` by default.
    cursor
      Character used for cursor. `▋` by default.
    noInit
      Do not initialise the animation when the termynal window is loaded.
      When set to `true`, the termynal window can be initialised by explicitly
      calling `Termynal.init()`. `false` by default.
    lineData
      Dynamically load termynal lines at instantiation. `null` by default.

    The content of the directive is a **yml-formatted** terminal transcript
    given as a *list of dictionaries*, with each list entry describing a
    single termynal line.
    The structure of the content is as follows::
      - value: terminal line content
        type: empty / input / progress
        prompt: prompt style
        progressPercent: maximum percent of a progress bar
        progressChar: *refer to te description above*
        typeDelay: *refer to te description above*
        cursor: *refer to te description above*
    Additionally, empty list elements will be translated to empty lines.
    For more information about customising termynal lines please refer to
    `termynal HTML line configuration`_.

    This Sphinx extension monitors the terminal transcript files for changes
    and regenerates the content pages that use them if a change is detected.

    .. _`termynal HTML configuration`: https://github.com/ines/termynal#customising-termynal
    .. _`termynal HTML line configuration`: https://github.com/ines/termynal#prompts-and-animations for description
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True
    option_spec = {i: directives.unchanged for i in TERMYNAL_ATTRS}

    def run(self):
        """Builds a termynal box."""
        env = self.state.document.settings.env
        options = self.options
        data_ty = 'data-ty-{}'
        data_ty_error = 'The *{}* parameter should be a {}.'

        # retrieve the path to the directory holding the code files
        st_term_dir = env.config.sphinx_term_termynal_dir
        assert isinstance(st_term_dir, str) or st_term_dir is None

        # get the terminal file name for this particular termynal box
        assert len(self.arguments) == 1, (
            'Just one argument -- terminal block id (possibly encoding the '
            'code file name -- expected')
        term_filename_id = self.arguments[0]
        assert term_filename_id.startswith('termynal:'), (
            'The terminal box label ({}) must start with the "termynal:" '
            'prefix.'.format(term_filename_id))
        assert not term_filename_id.endswith('.yml'), (
            'The terminal box label ({}) must not end with the ".yml" '
            'extension prefix.'.format(term_filename_id))
        # add the .yml extension as it is missing
        term_filename = '{}.yml'.format(term_filename_id[9:])

        # collect termynal attributes
        attributes = {}

        # prefix
        attr = 'prefix'
        attr_text = options.get(attr, None)
        if attr_text is not None:
            # validate
            if not isinstance(attr_text, str):
                raise ValueError(data_ty_error.format(attr, 'string'))
            # memorise
            attributes[data_ty.format(attr)] = attr_text
        # startDelay
        attr = 'startDelay'
        attr_text = options.get(attr, None)
        if attr_text is not None:
            # validate
            if not isinstance(attr_text, str) or not attr_text.isdigit():
                raise ValueError(data_ty_error.format(
                    attr, 'non-negative integer'))
            # memorise
            attributes[data_ty.format(attr)] = attr_text
        # typeDelay
        attr = 'typeDelay'
        attr_text = options.get(attr, None)
        if attr_text is not None:
            # validate
            if not isinstance(attr_text, str) or not attr_text.isdigit():
                raise ValueError(data_ty_error.format(
                    attr, 'non-negative integer'))
            # memorise
            attributes[data_ty.format(attr)] = attr_text
        # lineDelay
        attr = 'lineDelay'
        attr_text = options.get(attr, None)
        if attr_text is not None:
            # validate
            if not isinstance(attr_text, str) or not attr_text.isdigit():
                raise ValueError(data_ty_error.format(
                    attr, 'non-negative integer'))
            # memorise
            attributes[data_ty.format(attr)] = attr_text
        # progressLength
        attr = 'progressLength'
        attr_text = options.get(attr, None)
        if attr_text is not None:
            # validate
            if (not isinstance(attr_text, str) or not attr_text.isdigit()
                    or int(attr_text) < 1):
                raise ValueError(data_ty_error.format(
                    attr, 'positive integer'))
            # memorise
            attributes[data_ty.format(attr)] = attr_text
        # progressChar
        attr = 'progressChar'
        attr_text = options.get(attr, None)
        if attr_text is not None:
            # validate
            if not isinstance(attr_text, str):
                raise ValueError(data_ty_error.format(attr, 'string'))
            # memorise
            attributes[data_ty.format(attr)] = attr_text
        # cursor
        attr = 'cursor'
        attr_text = options.get(attr, None)
        if attr_text is not None:
            # validate
            if not isinstance(attr_text, str):
                raise ValueError(data_ty_error.format(attr, 'string'))
            # memorise
            attributes[data_ty.format(attr)] = attr_text
        # noInit
        attr = 'noInit'
        attr_text = options.get(attr, None)
        if attr_text is not None:
            # validate
            if (not isinstance(attr_text, str)
                    or attr_text.lower() not in ['true', 'false', '']):
                raise ValueError(data_ty_error.format(attr, 'boolean'))
            # memorise
            val = 'false' if attr_text.lower() == 'false' else 'true'
            attributes[data_ty.format(attr)] = val
        # lineData
        attr = 'lineData'
        attr_text = options.get(attr, None)
        if attr_text is not None:
            # validate
            if not isinstance(attr_text, str):
                raise ValueError(data_ty_error.format(
                    attr, 'string (Object[])'))
            # memorise
            attributes[data_ty.format(attr)] = attr_text

        # if the content is given explicitly, use it instead of loading a file
        if self.content:
            contents = '\n'.join(self.content)
        else:
            localised_directory = sphinx_term.localise_term_directory(
                env.srcdir,
                st_term_dir,
                ('sphinx_term_termynal_dir', 'termynal box content'))
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

        # read the yaml content
        try:
            contents_yaml = yaml.safe_load(contents)  # or {}
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as e:
            raise ValueError('Invalid termynal content YAML format: ', str(e))

        # create a termynal node
        box = termynal_box(label=term_filename_id, **attributes)
        # assign label and id (`ids=[nodes.make_id(term_filename_id)]`)
        self.options['name'] = term_filename_id
        self.add_name(box)

        # validate, process and embed each termynal line
        for line in contents_yaml:
            if line is None:
                line = {}
                line_value = ''
            elif isinstance(line, str):
                line_value = line
                line = {}
            elif isinstance(line, dict):
                # validate
                validate_termynal_line(line)

                # process
                if line.get('type', None) is None:
                    line['type'] = ''

                if 'value' in line:
                    line_value = line.get('value', '')
                    del line['value']
                else:
                    line_value = ''
            else:
                assert False, 'Unknown termynal line type.'

            # embed
            line_node = termynal_line(line_value.strip(), line_value, **line)
            box += line_node

        return [box]


def validate_termynal_line(line):
    """Validates a yaml termynal line (dictionary within the contents list)."""
    bad = set(line.keys()).difference(TERMYNAL_LINE_ATTRS + ['type', 'value'])
    if bad:
        raise ValueError('The following termynal line keys are '
                         'invalid: {}.'.format(bad))

    # value
    line_value = line.get('value', None)
    if line_value is not None and not isinstance(line_value, str):
        raise ValueError('Line value (*value* key for a line of termynal '
                         'directive) must be a string or not specified.'
                         '\n\n{}'.format(line_value))
    # type
    line_type = line.get('type', None)
    if line_type not in (None, '', 'input', 'progress'):
        raise ValueError('Line type (*type* key for a line of '
                         'termynal directive) must be one of '
                         '*input*, *progress* or not specified.'
                         '\n\n{}'.format(line_type))
    # prompt
    line_prompt = line.get('prompt', None)
    if line_prompt is not None:
        if not isinstance(line_prompt, str):
            raise ValueError('Prompt specifier (*prompt* key for a line '
                             'of termynal directive) must be a string.'
                             '\n\n{}'.format(line_prompt))
    # progressPercent
    line_progress = line.get('progressPercent', None)
    if line_progress is not None:
        if not isinstance(line_progress, int) or line_progress < 0:
            raise ValueError(
                'Prompt percentage (*progressPercent* key for a '
                'line of termynal directive) '
                'must be a non-negative integer.'
                '\n\n{}'.format(line_progress))
    # progressChar
    line_progresschar = line.get('progressChar', None)
    if line_progresschar is not None:
        if not isinstance(line_progresschar, str):
            raise ValueError('Progress cursor (*progressChar* key for a '
                             'line of termynal directive) must be a string.'
                             '\n\n{}'.format(line_progresschar))
    # typeDelay
    line_typedelay = line.get('typeDelay', None)
    if line_typedelay is not None:
        if (not isinstance(line_typedelay, int)
                or line_typedelay < 0):
            raise ValueError(
                'Typing delay (*typeDelay* key for a line of '
                'termynal directive) must be a non-negative integer.'
                '\n\n{}'.format(line_typedelay))
    # cursor
    line_cursor = line.get('cursor', None)
    if line_cursor is not None:
        if not isinstance(line_cursor, str):
            raise ValueError('Prompt cursor (*cursor* key for a line of '
                             'termynal directive) must be a string.'
                             '\n\n{}'.format(line_cursor))


def validate_termynal_lines(app, doctree, docname):
    """
    Ensures that all termynal_line nodes are within a termynal_box node.

    This function is hooked up to the `doctree-resolved` Sphinx event.
    """
    # only go through non-empty documents
    if doctree is None:
        return
    # get termynal lines
    termynal_lines = doctree.traverse(termynal_line)
    # skip pages without at least one termynal line
    if not termynal_lines:
        return

    for line in termynal_lines:
        if not isinstance(line.parent, termynal_box):
            raise Exception('Each termynal line must be embedded '
                            'within a termynal box.')


def inject_termynal_init(app, doctree, docname):
    """
    Injects call to the termynal JavaScript library in documents that have
    termynal boxes.

    This function is hooked up to the `doctree-resolved` Sphinx event.
    """
    # only go through non-empty documents
    if doctree is None:
        return
    # get termynal boxes
    termynal_boxes = doctree.traverse(termynal_box)
    # skip pages without at least one termynal box
    if not termynal_boxes:
        return

    # get termynal box ids
    termynal_ids = []
    for box in termynal_boxes:
        ids = box.attributes['ids']
        ids = [i for i in ids if i.startswith('termynal-')]
        assert len(ids) == 1, 'Only one id is expected'
        termynal_ids.append('#{}'.format(ids[0]))
    assert termynal_ids, 'With termynal boxes available, ids cannot be empty'

    rel_root = os.path.relpath('.', os.path.dirname(docname))  # app.outdir
    rel_termynal = os.path.join(rel_root, '_static', 'termynal.js')

    termynal_function = ('\n\n'
                         '    <script src="{}" '
                         'data-termynal-container="{}">'
                         '</script>\n'.format(rel_termynal,
                                              '|'.join(termynal_ids)))
    # `format='html'` is crucial to avoid escaping html characters
    script_node = nodes.raw(
        termynal_function, termynal_function, format='html')
    # add the call node to the document
    doctree.append(script_node)


def assign_reference_title(app, document):
    """
    Update the labels record of the standard environment to allow referencing
    termynal boxes.
    """
    # get the standard domain
    domain = app.env.get_domain('std')

    # go through every termynal box
    for node in document.traverse(termynal_box):
        # every termynal box must have exactly one name starting with
        # 'termynal:'
        assert node['names']
        assert len(node['names']) == 1
        node_name = node['names'][0]

        assert node_name.startswith('termynal:'), (
            'termynal box ids must start with termynal:')
        refname = REFNAME

        # every termynal box has a single id
        assert len(node['ids']) == 1
        node_id = node['ids'][0]

        # get the document name
        docname = app.env.docname

        # every termynal box should *already* be referenceable without a title
        assert node_name in domain.anonlabels
        assert domain.anonlabels[node_name] == (docname, node_id)

        # allow this termynal box to be referenced with the default
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
    """Includes termynal static files only on pages that use the module."""
    # only go through non-empty documents
    if doctree is None:
        return

    # get termynal boxes
    termynal_boxes = doctree.traverse(termynal_box)
    # skip pages without at least one termynal box
    if not termynal_boxes:
        return

    # ensure that custom files were included
    for css_file in STATIC_CSS_FILES:
        _css_file = os.path.basename(css_file)
        if not sphinx_term.is_css_registered(app, _css_file):
            app.add_css_file(_css_file)
    for js_file in STATIC_JS_FILES:
        _js_file = os.path.basename(js_file)
        # skip termynal*.js, it's handled by the inject_termynal_init function
        if not (sphinx_term.is_js_registered(app, _js_file)
                or _js_file.startswith('termynal')):
            app.add_js_file(_js_file)

    # add external dependencies
    script_files = [os.path.basename(i) for i in context['script_files']]
    for stub, path in DEPENDENCIES.items():
        if sphinx_term.is_js_registered(app, path) or stub in script_files:
            continue
        app.add_js_file(path)
    for _, path in STYLES.items():
        if sphinx_term.is_css_registered(app, path):
            continue
        app.add_css_file(path)


def setup(app):
    """
    Sets up the Sphinx extension for the `termynal` directive.
    """
    # register two Sphinx config values used for the extension
    app.add_config_value('sphinx_term_termynal_dir', None, 'env')

    # register the custom docutils nodes with Sphinx
    app.add_node(
        termynal_box,
        html=(visit_termynal_box_node, depart_termynal_box_node),
        latex=(visit_termynal_box_node_, depart_termynal_box_node_),
        text=(visit_termynal_box_node_, depart_termynal_box_node_)
    )
    app.add_node(
        termynal_line,
        html=(visit_termynal_line_node, depart_termynal_line_node),
        latex=(visit_termynal_line_node_, depart_termynal_line_node_),
        text=(visit_termynal_line_node_, depart_termynal_line_node_)
    )

    # register the custom role and directives with Sphinx
    app.add_directive('termynal', Termynal)

    # connect custom hooks to the Sphinx build process
    app.connect('doctree-read', assign_reference_title)
    app.connect('doctree-resolved', inject_termynal_init)
    app.connect('doctree-resolved', validate_termynal_lines)
    # ...ensure the required static files are **copied** into the build
    app.connect('builder-inited', include_static_files)
    # ...ensure that relevant html output pages **load** the static files
    app.connect('html-page-context', load_static_files)

    return {'version': sphinx_term.VERSION}
