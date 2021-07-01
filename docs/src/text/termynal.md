(sec:termynal)=

# `termynal` module #

The `sphinx_term.termynal` [Sphinx] extension implements the `termynal`
directive, which builds [termynal] terminal windows.
In this section we discuss various aspects of this directive in the context
of [Jupyter Book].
Instructions on how to install and enable the extension are provided
[here](sec:sphinx-term).
A technical documentation of this extension can be found in the [README] file
of the [so-cool/sphinx-term] GitHub repository.

:::{note}
Each example of the `termynal` embedded on this page is displayed along
the raw Markdown source used to generate it.
To switch between the two views use the tabs -- *Outcome* and *Syntax* --
visible above each terminal window.
:::

## Simple terminal window ##

Basic [termynal] windows are embedded with the `termynal` directive like so:

:::{tabbed} Outcome
```{termynal} termynal:example
---
typeDelay: 40
lineDelay: 700
---
- value: pip install spacy
  type: input
- type: progress
- Successfully installed spacy
-
- value: python -m spacy download en
  type: input
- type: progress
- Installed model 'en'
-
- value: python
  type: input
- value: import spacy
  type: input
  prompt: '>>>'
- value: nlp = spacy.load('en')
  type: input
  prompt: '>>>'
- value: doc = nlp(u'Hello world')
  type: input
  prompt: '>>>'
- value: print([(w.text, w.pos_) for w in doc])
  type: input
  prompt: '>>>'
- "[('Hello', 'INTJ'), ('world', 'NOUN')]"
```
:::
:::{tabbed} Syntax
````text
```{termynal} termynal:example
---
typeDelay: 40
lineDelay: 700
---
- value: pip install spacy
  type: input
- type: progress
- Successfully installed spacy
-
- value: python -m spacy download en
  type: input
- type: progress
- Installed model 'en'
-
- value: python
  type: input
- value: import spacy
  type: input
  prompt: '>>>'
- value: nlp = spacy.load('en')
  type: input
  prompt: '>>>'
- value: doc = nlp(u'Hello world')
  type: input
  prompt: '>>>'
- value: print([(w.text, w.pos_) for w in doc])
  type: input
  prompt: '>>>'
- "[('Hello', 'INTJ'), ('world', 'NOUN')]"
```
````
:::

:::{note}
You can restart the animation by clicking the button below.
If the termynal window is reset while it is still being rendered,
the animation will break.

<button type="button"
        class="btn btn-primary"
        onclick="new Termynal('#termynal-example')">Restart animation</button>
:::

This approach requires you to list the terminal output directly within the
`termynal` directive.
Additionally, each [termynal] window **needs** to be tagged with an id
prefixed with `termynal:`, e.g., `termynal:example` for the
{ref}`terminal box above <termynal:example>`.

## Terminal content structure ##

The content of the `termynal` directive is a **yml-formatted list** of lines
to be displayed by the terminal (i.e., the terminal transcript).
Each element of this list can either be:
- an **empty** element -- indicating a plain, empty line;
- a **string** -- specifying a plain line of terminal *output* text; or
- a **dictionary** -- defining more complex line style.

Each line defined as a *dictionary* supports the following **optional** keys:
- `value` (default *empty string*) -- the content of the termynal
  line given as a string;
- `type` (default *none*) -- the line type where:
  * `input` indicates that the termynal line is an input,
  * `progress` creates a progress bar (`value` is not required), and
  * *empty string* (`''`) or *undefined* to get a plain *output* line --
    the default behaviour;
- `prompt` (default `$`) -- a string specifying the prompt style;
- `progressPercent` (default `100`) -- the maximum percent of the
  `progress` bar;
- `progressChar` (default `█`) -- the character used to build the
  `progress` bar (*see below for more details*);
- `typeDelay` (default `90`) -- the delay between each typed
  character given in milliseconds (*see below for more details*); and
- `cursor` (default `▋`) -- the character used as the cursor
  (*see below for more details*).

For more information about customising termynal lines refer to the official
documentation of [termynal lines][termynal-line].

## Configuring terminal window ##

The `termynal` directive takes a number of **optional** parameters outlined in
the table below.
(See the official documentation of [termynal boxes][termynal-conf] for more
information.)

| Parameter        | Default | Description                                    |
| ---------------- | ------- | ---------------------------------------------- |
| `prefix`         | `ty`    | The prefix used for data attributes.           |
| `startDelay`     | `600`   | The delay before animation, given in milliseconds. |
| `typeDelay`      | `90`    | The delay between displaying each typed character, given in milliseconds. |
| `lineDelay`      | `1500`  | The delay between displaying each line, given in milliseconds. |
| `progressLength` | `40`    | The number of characters used when displaying a progress bar. |
| `progressChar`   | `█`     | The character used for building progress bars. |
| `cursor`         | `▋`     | The character used for displaying the cursor. |
| `noInit`         | `false` | Whether to initialise the animation when the termynal window is loaded. When set to `true`, the termynal window can be initialised by explicitly calling `Termynal.init()`. |
| `lineData`       | `null`  | The sequence used to dynamically load termynal lines at instantiation. |

## Loading terminal window from file ##

Alternatively, the [termynal] box can load its content from a file.
To this end, the [`sphinx_term_termynal_dir`] [Sphinx] configuration parameter
must point to a directory holding a collection of terminal content files.
These files must have `.yml` extension -- see [this directory] for an example.
Then, a `.yml` file is loaded into a [termynal] window with a specially
formatted tag: the base name of the file prepended with the `termynal:` prefix
and without the `.yml` extension.
For example, for the [`example2.yml`] file, the corresponding [termynal] box
is created like so:

:::{tabbed} Outcome
```{termynal} termynal:example2
---
typeDelay: 40
lineDelay: 700
---
```
:::
:::{tabbed} Syntax
````text
```{termynal} termynal:example2
---
typeDelay: 40
lineDelay: 700
---
```
````
:::

:::{note}
You can restart the animation by clicking the button below.
If the termynal window is reset while it is still being rendered,
the animation will break.

<button type="button"
        class="btn btn-primary"
        onclick="new Termynal('#termynal-example2')">Restart animation</button>
:::

Note that if both the terminal file exists and the terminal content is provided
directly within the `termynal` directive, the latter takes precedence.
For example, for the [`example3.yml`] file, the content of the terminal box
tagged with `termynal:example3` will display the explicitly listed code
instead of loading its content from the [`example3.yml`] file like so:

:::{tabbed} Outcome
```{termynal} termynal:example3
---
typeDelay: 40
lineDelay: 700
---
- value: npm uninstall react
  type: input
  prompt: ▲
- Are you sure you want to uninstall 'react'?
- value: y
  type: input
  prompt: (y/n)
  typeDelay: 1000
- type: progress
  progressChar: '·'
- Uninstalled 'react'
- value: node
  type: input
  prompt: ▲
- value: Array(5).fill('🌈')
  type: input
  prompt: '>'
- "['🌈', '🌈', '🌈', '🌈', '🌈']"
- value: cd ~/repos
  type: input
  prompt: ▲
- value: git checkout branch master
  type: input
  prompt: ▲ ~/repos
- value: git commit -m "Fix things"
  type: input
  prompt: ▲ ~/repos (master)
```
:::
:::{tabbed} Syntax
````text
```{termynal} termynal:example3
---
typeDelay: 40
lineDelay: 700
---
- value: npm uninstall react
  type: input
  prompt: ▲
- Are you sure you want to uninstall 'react'?
- value: y
  type: input
  prompt: (y/n)
  typeDelay: 1000
- type: progress
  progressChar: '·'
- Uninstalled 'react'
- value: node
  type: input
  prompt: ▲
- value: Array(5).fill('🌈')
  type: input
  prompt: '>'
- "['🌈', '🌈', '🌈', '🌈', '🌈']"
- value: cd ~/repos
  type: input
  prompt: ▲
- value: git checkout branch master
  type: input
  prompt: ▲ ~/repos
- value: git commit -m "Fix things"
  type: input
  prompt: ▲ ~/repos (master)
```
````
:::

:::{note}
You can restart the animation by clicking the button below.
If the termynal window is reset while it is still being rendered,
the animation will break.

<button type="button"
        class="btn btn-primary"
        onclick="new Termynal('#termynal-example3')">Restart animation</button>
:::

## Referencing terminal window ##

Finally, each terminal window can be hyper-linked using the MyST Markdown
[`ref` role].
To reference a [termynal] terminal box with the standard "*terminal box*"
hyper-link use the `` {ref}`termynal:tag` `` syntax, where `termynal:tag` is
the tag of the destination terminal window.

:::{panels}
E.g., see this {ref}`termynal:example`.

---

```md
E.g., see this {ref}`termynal:example`.
```
:::

The hyper-link text can also be personalised with the
`` {ref}`custom hyper-link text <termynal:tag>` `` syntax.

:::{panels}
E.g., see this {ref}`awesome termynal log <termynal:example>`.

---

```md
E.g., see this {ref}`awesome termynal log <termynal:example>`.
```
:::

[termynal]: https://github.com/ines/termynal
[sphinx]: https://www.sphinx-doc.org/
[jupyter book]: https://jupyterbook.org/
[readme]: https://github.com/So-Cool/sphinx-term#readme
[so-cool/sphinx-term]: https://github.com/So-Cool/sphinx-term
[termynal-conf]: https://github.com/ines/termynal#customising-termynal
[termynal-line]: https://github.com/ines/termynal#prompts-and-animations
[this directory]: https://github.com/So-Cool/sphinx-term/tree/master/docs/src/termynal_files
[`sphinx_term_termynal_dir`]: https://github.com/So-Cool/sphinx-term/blob/master/docs/_config.yml#L57
[`example2.yml`]: https://github.com/So-Cool/sphinx-term/blob/master/docs/src/termynal_files/example2.yml
[`ref` role]: https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html#targets-and-cross-referencing
[`example3.yml`]: https://github.com/So-Cool/sphinx-term/blob/master/docs/src/termynal_files/example3.yml
