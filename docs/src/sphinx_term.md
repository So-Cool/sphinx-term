(sec:sphinx-term)=
# Using sphinx-term #

This [Jupyter Book] shows how to use the [sphinx-term] [Sphinx] extension,
which is hosted in the [so-cool/sphinx-term] GitHub repository and published
on [PyPI].
It implements **vivacious terminal transcripts** that can be easily embedded
in your [Sphinx] documentation and [Jupyter Book] pages.
The [sphinx-term] extension relies on two web terminal window packages:
* [termynal]; and
* [cssterm].

:::{seealso}
Additional (technical) documentation of this extension can be found in the
[`README.md`] file distributed within the [so-cool/sphinx-term] GitHub
repository.
:::

## Installing and activating sphinx-term ##

To get started with [sphinx-term], first install it via `pip`:
```bash
pip install sphinx-term
```
Then, add the `cssterm` and/or `termynal` module of the `sphinx_term`
extension to the `extra_extensions` configuration section of your
[Jupyter Book] `_config.yml`:
```yaml
sphinx:
  extra_extensions:
    - sphinx_term.cssterm
    - sphinx_term.termynal
```
Finally, configure the source directory for each plugin if you decide to
load the terminal content from external files:
```yaml
sphinx:
  config:
    sphinx_term_cssterm_dir: src/cssterm_files/
    sphinx_term_termynal_dir: src/termynal_files/
```
See the [`_config.yml`] file of this documentation for reference.

[Jupyter Book]: https://jupyterbook.org/
[sphinx-term]: https://github.com/So-Cool/sphinx-term
[so-cool/sphinx-term]: https://github.com/So-Cool/sphinx-term
[Sphinx]: https://www.sphinx-doc.org/
[PyPI]: https://pypi.org/project/sphinx-term
[termynal]: https://github.com/ines/termynal
[cssterm]: https://github.com/nstephens/cssterm
[`README.md`]: https://github.com/So-Cool/sphinx-term#readme
[`_config.yml`]: https://github.com/So-Cool/sphinx-term/blob/master/docs/_config.yml#L38-L41
