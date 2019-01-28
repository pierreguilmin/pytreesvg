# todo

| emoji        | meaning                      | code           |
| :----------: | :--------------------------- | :------------- |
| :sos:        | critical bug                 | `:sos:`        |
| :warning:    | bug                          | `:warning:`    |
| :flashlight: | simplification/clarification | `:flashlight:` |
| :clipboard:  | comment                      | `:clipboard:`  |
| :sparkles:   | typos & style                | `:sparkles:`   |
| :tada:       | new feature                  | `:tada:`       |
| :cloud:      | minor modification           | `:cloud:`      |

## General
- [x] :tada: find a license (https://choosealicense.com/)
- [ ] :tada: add pip and virtualenv configuration
- [ ] :tada: package code and upload it to PyPI and conda
- [ ] :tada: add codacy/codecoverage GitHub marketplace extensions
- [ ] :tada: add command-line extension
- [ ] :tada: create `README.md` and `index.rst` gif demonstration
- [ ] :tada: advertise project on StackOverflow Q&A
- [ ] :tada: add more descriptive but also funny/pretty examples

### Travis CI
- [ ] :tada: add Windows support (update `travis/install_conda.sh` and `.travis.yml`)

### Sphinx
- [x] :flashlight: necessary to add `.. testsetup::` at the beginning of every module for the doctest to work
- [x] :sparkles: switch math rendering from `imgmath` to `mathjax` (faster builds, cleaner outputs, lighter doc, ...)
- [x] :tada: add contact section
- [x] :sparkles: collapsible sections for `.svg` output

## `node_svg.py`
- `Node_SVG_Style`
    - [x] :tada: extend the set of base colors to match SVG recommendations
    - [x] :tada: add support for all SVG color notations (`#2f0`, `rgb(255,255,127)`, `rgb(100%,100%,32%)`, ...)

- `Node_SVG`
    - [ ] :sos: visualization error with vertical linear gradient applied to `line` svg object, switch to `rect` object?
    - [ ] :warning: linear gradient from top to bottom, doesn't look good for horizontal lines
    - [ ] :tada: multiple shapes support
    - [ ] :tada: text inside nodes (and automatic ellipsis)
    - [ ] :tada: possibility to create random tree
    - [ ] :tada: multiple layout (aligned left, circle, ...)
    - [ ] :tada: default tree style options (basic, red to blue, ...)
    - [ ] :tada: allow easy tree building by parsing a string representing the tree

## Various
- [ ] What about representing a tree by a matrix?
- [ ] Use the website https://validator.w3.org/check to verify the `.svg` file created?
- [ ] Take a look at `.svg` possible interactions like `onmouseover`, `onclick`, ...
- [ ] Check possible code optimisation
- [ ] Check max recursion depth Python and document it
