[![build status](https://travis-ci.com/PierreGuilmin/pytreesvg.svg?branch=master)](https://travis-ci.com/PierreGuilmin/pytreesvg)
[![documentation status](https://readthedocs.org/projects/pytreesvg/badge/?version=latest)](https://pytreesvg.readthedocs.io/en/latest/?badge=latest)

:construction: work in progress... :construction:

# :herb: pytreesvg

This project is a lightweight Python module to render SVG trees like the following:

<!-- top centered demo image -->
<p align="center">
    <img alt="basic tree" src="images/basic_tree.svg">
</p>

The documentation of **:herb: pytreesvg** is available at https://pytreesvg.readthedocs.io/en/latest/.

**:herb: pytreesvg** guarantees that the output SVG file strictly follows the [W3C SVG 1.1 (Second Edition) Recommendation](https://www.w3.org/TR/2011/REC-SVG11-20110816/).

This module aims to be extremely basic and simple of use, thus it is based on no other existing modules. If you are looking for something more complex please take a look at [Graphviz](https://www.graphviz.org/) and the existing Python implementations.

***

## Work with this repository

### Clone the repository

[![build status](https://travis-ci.com/PierreGuilmin/pytreesvg.svg?branch=master)](https://travis-ci.com/PierreGuilmin/pytreesvg)

To clone this repository on your local computer please run:
```bash
$ git clone https://github.com/PierreGuilmin/pytreesvg.git
```

:warning: This project is still under development and not stable yet.

### Setup a Python conda environment on your local computer

> :point_up: We assume you have `conda` installed on your computer, otherwise please take a look at [conda documentation](https://docs.conda.io/en/latest/) and [conda cheat sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html).

The repository was written and tested under `Python 3.6`. You can see the requirements under [`environment.yml`](environment.yml). To create the conda environment named `pytreesvg_env` (the environment used by the project), please run the following command:
```bash
# create the conda environment
$ conda env create --file environment.yml
```

Some useful command lines to work with this conda environment:
```bash
# activate the conda environment
$ source activate pytreesvg_env

# deactivate the conda environment
$ source deactivate

# remove the conda environment
$ conda env remove --name pytreesvg_env
```

### Documentation

[![documentation status](https://readthedocs.org/projects/pytreesvg/badge/?version=latest)](https://pytreesvg.readthedocs.io/en/latest/?badge=latest)

The documentation of **:herb: pytreesvg** is available at https://pytreesvg.readthedocs.io/en/latest/.

It is built with Sphinx and updated every time a commit is pushed on the GitHub repository master branch.

### Repository structure
- **`doc/`**: directory holding the Sphinx related files.

- **`images/`**: project images.

- **`pytreesvg/`**: the main Python module.

- **`temp/`**: drafts, temporary files and old scripts.
  > :warning: This directory should not be versionned.

- **`test/`**: Python `unittest` directory for the `pytreesvg` module.

- **`travis/`**: Travis CI related directory.

### Emoji commit code table

Please use the following table to commit code:

| emoji        | meaning                      | code           |
| :----------: | :--------------------------- | :------------- |
| :sos:        | critical bug                 | `:sos:`        |
| :warning:    | bug                          | `:warning:`    |
| :flashlight: | simplification/clarification | `:flashlight:` |
| :clipboard:  | comment                      | `:clipboard:`  |
| :sparkles:   | typos & style                | `:sparkles:`   |
| :tada:       | new feature                  | `:tada:`       |
| :cloud:      | minor modification           | `:cloud:`      |

For example if you want to commit a new rocket feature — `🎉 new feature, flying rocket!` — please do:
```diff
# bad syntax
- $ git commit -m 'new feature, flying rocket!'

# good syntax
+ $ git commit -m ':tada: new feature, flying rocket!'
```

### Notes
The conda environment was created with the following commands:
```bash
# create the conda environment
$ conda create --name pytreesvg_env python=3.6 sphinx sphinx_rtd_theme
$ source activate pytreesvg_env
$ pip install sphinxcontrib-napoleon
```

And the requirements were exported with the following command:
```bash
# export the current conda environment requirements as .yml, we remove
#   - the final "prefix: ..." line
#   - some macOS specific modules not available on Linux (libcxx and libcxxabi)
$ conda env export --no-builds --name pytreesvg_env | grep -E -v "^prefix|libcxx|libcxxabi" > environment.yml
```
