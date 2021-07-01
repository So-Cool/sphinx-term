# Web Dependencies #
The `sphinx-term` extension builds upon two web terminal window packages:
[termynal] and [cssterm], both of which are loaded into this repository as
git submodules.

## termynal ##
The [`sphinx-term.termynal`] Python module requires the following CSS and JS
files distributed as part of the [termynal] package:
- `termynal.css` and
- `termynal.js`.

[termynal] is distributed under the **MIT** license.

> The MIT License (MIT)
>
> Copyright (C) 2017 Ines Montani
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.

## cssterm ##
The [`sphinx-term.cssterm`] Python module requires the following CSS and JS
files distributed as part of the [cssterm] package:
- `css/cssterm.css` and
- `scripts/cssterm.js`.

Additionally, [cssterm] depends on [jQuery], which is loaded from a
[CDN](http://code.jquery.com/jquery-latest.js).

[cssterm] is distributed **without** a license.

[termynal]: https://github.com/ines/termynal
[cssterm]: https://github.com/nstephens/cssterm
[`sphinx-term.termynal`]: ../termynal.py
[`sphinx-term.cssterm`]: ../cssterm.py
[jQuery]: https://github.com/jquery/jquery
