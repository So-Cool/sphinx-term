[![Licence][licence-badge]][licence-link]
[![Python][python-badge]][python-link]
[![PyPI][pypi-badge]][pypi-link]
[![Documentation][doc-badge]][doc-link]

[licence-badge]: https://img.shields.io/github/license/so-cool/sphinx-term.svg
[licence-link]: https://github.com/so-cool/sphinx-term/blob/master/LICENCE
[python-badge]: https://img.shields.io/badge/python-3.5-blue.svg
[python-link]: https://github.com/so-cool/sphinx-term
[pypi-badge]: https://img.shields.io/pypi/v/sphinx-term.svg
[pypi-link]: https://pypi.org/project/sphinx-term
[doc-badge]: https://img.shields.io/badge/read-documentation-blue.svg
[doc-link]: https://so-cool.github.io/sphinx-term

# :computer: Terminal extension for Jupyter Book (and Sphinx) #

This repository holds *terminal* extensions for [Sphinx], designed to be used
with the [Jupyter Book] platform.
It implements **vivacious terminal transcripts** that can be easily embedded
in your [Sphinx] documentation and [Jupyter Book] pages.
The `sphinx-term` extension relies on two web terminal window packages:
* [termynal]; and
* [cssterm].

**This readme file holds a technical documentation of the `sphinx-term`
extension.
For a [Jupyter Book] user guide and usage example of the terminal boxes
visit the [example page] hosted on GitHub Pages, the source of which is
available in the [docs] folder of this repository.**

> This *readme* file uses [Jupyter Book]'s [MyST Markdown] syntax for **roles**
  and **directives** -- see [MyST overview] for more details.
  For use with [Sphinx], please refer to the [reStructuredText] syntax.

## :snake: Installing `sphinx-term` ##

To get started with `sphinx-term`, first install it via `pip`:
```bash
pip install sphinx-term
```
then, add the `cssterm` and/or `termynal` module of the `sphinx_term`
extension to the Sphinx `extensions` list in your `conf.py`
```Python
...
extensions = [
    'sphinx_term.cssterm',
    'sphinx_term.termynal'
]
...
```

## :keyboard: cssterm directive ##

The [`sphinx_term.cssterm`](sphinx_term/cssterm.py) module defines the
`cssterm` directive, which is used for building [cssterm] terminal windows.

### Usage ###

A *[cssterm] terminal box* is included with the `cssterm` directive:

````text
```{cssterm} cssterm:my-id
$ echo "My terminal transcript"
My terminal transcript
```
````

Each [cssterm] box can be referenced with its name using the `ref` role,
e.g., `` {ref}`cssterm:my-id` ``, which produces *terminal box* hyper-link.
The default hyper-link text can be changed with with the folowing `ref` role
syntax: `` {ref}`custom hyper-link text <cssterm:my-id>` ``.
See the [MyST Markdown documentation] for more details.

### Configuration parameters ###

The `cssterm` extension uses one [Sphinx] configuration parameter:

* `sphinx_term_cssterm_dir` (**required** when loading the box content
  from a file) -- defines the path to a directory holding files with content
  (terminal transcript) of each terminal box.

### Arguments, parameters and content ###

Each [cssterm] box has one **required** argument that specifies
the *unique* id of this particular terminal block.
This id **must** start with the `cssterm:` prefix.
The content of a [cssterm] box can **either** be provided explicitly within the
directive, **or** -- when the content is left empty -- it is pulled from a
terminal transcript file whose name is derived from the terminal box id,
and which should be located in the directory specified via the
`sphinx_term_cssterm_dir` configuration parameter.
The terminal transcript file name is expected to be the [cssterm] block id
**without** the `cssterm:` prefix and **with** the `.log` extension.
For example, for a [cssterm] block with `cssterm:my_log` id, the terminal
transcript file should be named `my_code.log`.
The `sphinx_term.cssterm` [Sphinx] extension *monitors* the code files for
changes and automatically regenerates the affected pages.

## :keyboard: termynal directive ##

*Work in progress.*

---

> The CSS and JS files used by this [Sphinx] extension are loaded as
  git submodules into the [`sphinx_term/_static`](sphinx_term/_static)
  directory of this repository.

[sphinx]: https://www.sphinx-doc.org/
[jupyter book]: https://jupyterbook.org/
[termynal]: https://github.com/ines/termynal
[cssterm]: https://github.com/nstephens/cssterm
[example page]: https://so-cool.github.io/sphinx-term
[doc]: docs
[myst markdown]: https://myst-parser.readthedocs.io/
[myst overview]: https://jupyterbook.org/content/myst.html
[reStructuredText]: https://docutils.sourceforge.io/rst.html
[MyST Markdown documentation]: https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html#targets-and-cross-referencing
