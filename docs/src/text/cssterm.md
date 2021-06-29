(sec:cssterm)=

# `cssterm` module #

The `sphinx_term.cssterm` [Sphinx] extension implements the `cssterm`
directive, which builds [cssterm] terminal windows.
In this section we discuss various aspects of this directive in the context
of [Jupyter Book].
Instructions on how to install and enable the extension are provided
[here](sec:sphinx-term).
A technical documentation of this extension can be found in the [README] file
of the [so-cool/sphinx-term] GitHub repository.

:::{note}
Each example of the `cssterm` embedded on this page is displayed along
the raw Markdown source used to generate it.
To switch between the two views use the tabs -- *Outcome* and *Syntax* --
visible above each terminal window.
:::

## Simple terminal window ##

Basic [cssterm] windows are embedded with the `cssterm` directive like so:

:::{tabbed} Outcome
```{cssterm} cssterm:local
$ uname -a
Darwin MacBook-Pro 19.6.0 Darwin Kernel Version 19.6.0: Thu May  6 00:48:39 PDT 2021; root:xnu-6153.141.33~1/RELEASE_X86_64 x86_64

# dmesg | grep ioDevice
+ IOAudioDevice[<ptr>]::protectedCompletePowerStateChange() - current = 2 - pending = 2
- IOAudioDevice[<ptr>]::protectedCompletePowerStateChange() - current = 2 - pending = 2 returns 0x0
+ IOAudioDevice[<ptr>]::protectedCompletePowerStateChange() - current = 2 - pending = 2
- IOAudioDevice[<ptr>]::protectedCompletePowerStateChange() - current = 2 - pending = 2 returns 0x0
+ IOAudioDevice[<ptr>]::audioEngineStarting() - numRunningAudioEngines = 0
- IOAudioDevice[<ptr>]::audioEngineStarting() - numRunningAudioEngines = 1
```
:::
:::{tabbed} Syntax
````text
```{cssterm} cssterm:local
$ uname -a
Darwin MacBook-Pro 19.6.0 Darwin Kernel Version 19.6.0: Thu May  6 00:48:39 PDT 2021; root:xnu-6153.141.33~1/RELEASE_X86_64 x86_64

# dmesg | grep ioDevice
+ IOAudioDevice[<ptr>]::protectedCompletePowerStateChange() - current = 2 - pending = 2
- IOAudioDevice[<ptr>]::protectedCompletePowerStateChange() - current = 2 - pending = 2 returns 0x0
+ IOAudioDevice[<ptr>]::protectedCompletePowerStateChange() - current = 2 - pending = 2
- IOAudioDevice[<ptr>]::protectedCompletePowerStateChange() - current = 2 - pending = 2 returns 0x0
+ IOAudioDevice[<ptr>]::audioEngineStarting() - numRunningAudioEngines = 0
- IOAudioDevice[<ptr>]::audioEngineStarting() - numRunningAudioEngines = 1
```
````
:::

This approach requires you to list the terminal output directly within the
`cssterm` directive.
Additionally, each [cssterm] window needs to be tagged with with an id prefixed
with `cssterm:`, e.g., `cssterm:local` for the
{ref}`terminal box above <cssterm:local>`.

## Loading terminal window from file ##

Alternatively, the [cssterm] box can load its content from a file.
To this end, the [`sphinx_term_cssterm_dir`] [Sphinx] configuration parameter
must point to a directory holding a collection of terminal content files.
These files must have `.log` extensions -- see [this directory] for an example.
Then, a `.log` file is loaded into a [cssterm] window with a specially
formatted tag: the base name of the file prepended with the `cssterm:` prefix
and without the `.log` extension.
For example, for the [`demo.log`] file, the corresponding [cssterm] box is
created like so:

:::{tabbed} Outcome
```{cssterm} cssterm:demo
```
:::
:::{tabbed} Syntax
````text
```{cssterm} cssterm:demo
```
````
:::

Note that if both the terminal file exists and the terminal content is provided
directly within the `cssterm` directive, the latter takes precedence.
For example, for the [`overwrite.log`] file, the content of the terminal box
tagged with `cssterm:overwrite` will display the explicitly listed code instead
of loading its content from the [`overwrite.log`] file like so:

:::{tabbed} Outcome
```{cssterm} cssterm:overwrite
$ tree -d .
.
├── docs
│   └── src
│       ├── cssterm_files
│       ├── img
│       └── text
├── sphinx_term
│   └── _static
│       ├── cssterm
│       │   ├── css
│       │   └── scripts
│       └── termynal
```
:::
:::{tabbed} Syntax
````text
```{cssterm} cssterm:overwrite
$ tree -d .
.
├── docs
│   └── src
│       ├── cssterm_files
│       ├── img
│       └── text
├── sphinx_term
│   └── _static
│       ├── cssterm
│       │   ├── css
│       │   └── scripts
│       └── termynal
```
````
:::

## Referencing terminal window ##

Finally, each terminal window can be hyper-linked using the MyST Markdown
[`ref` role].
To reference a [cssterm] terminal box with the standard "*terminal box*"
hyper-link use the `` {ref}`cssterm:tag` `` syntax, where `cssterm:tag` is the
tag of the destination terminal window.

:::{panels}
E.g., see this {ref}`cssterm:local`.

---

```md
E.g., see this {ref}`cssterm:local`.
```
:::

The hyper-link text can also be personalised with the
`` {ref}`custom hyper-link text <cssterm:tag>` `` syntax.

:::{panels}
E.g., see this {ref}`awesome terminal log <cssterm:local>`.

---

```md
E.g., see this {ref}`awesome terminal log <cssterm:local>`.
```
:::

[cssterm]: https://github.com/nstephens/cssterm
[sphinx]: https://www.sphinx-doc.org/
[jupyter book]: https://jupyterbook.org/
[readme]: https://github.com/So-Cool/sphinx-term#readme
[so-cool/sphinx-term]: https://github.com/So-Cool/sphinx-term
[this directory]: https://github.com/So-Cool/sphinx-term/tree/master/docs/src/cssterm_files
[`sphinx_term_cssterm_dir`]: https://github.com/So-Cool/sphinx-term/blob/master/docs/_config.yml#L55
[`demo.log`]: https://github.com/So-Cool/sphinx-term/blob/master/docs/src/cssterm_files/demo.log
[`ref` role]: https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html#targets-and-cross-referencing
[`overwrite.log`]: https://github.com/So-Cool/sphinx-term/blob/master/docs/src/cssterm_files/overwrite.log
