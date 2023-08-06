# NbHub 💫
[![Build Status](https://travis-ci.org/duarteocarmo/nbhub.svg?branch=master)](https://travis-ci.org/duarteocarmo/nbhub) [![Coverage Status](https://coveralls.io/repos/github/duarteocarmo/nbhub/badge.svg?branch=master&service=github)](https://coveralls.io/github/duarteocarmo/nbhub?branch=master) [![PyPI version shields.io](https://img.shields.io/pypi/v/nbhub.svg)](https://pypi.python.org/pypi/nbhub/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/nbhub.svg)](https://pypi.org/project/nbhub/) [![PyPI downloads](https://img.shields.io/pypi/dm/nbhub.svg)](https://pypistats.org/packages/nbhub) [![GitHub license](https://img.shields.io/github/license/duarteocarmo/nbhub.svg)](https://github.com/duarteocarmo/nbhub/blob/master/LICENSE) [![made with: Vim](https://img.shields.io/badge/made%20with-Vim-019331)](https://github.com/vim/vim) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
<!-- [![nbhub](https://github.com/duarteocarmo/nbhub/raw/master/assets/logo.png)](https://nbhub.duarteocarmo.com) -->

A command-line application for sharing jupyter notebooks to the web. 

*Simple, minimal, hacky.*

**This is alpha! Check the [roadmap](#roadmap) and don't blow up my server.**

## Installation

NbHub requires pyhton 3.6 or newer. 

```bash
$ pip install nbhub
```

I actually recommend you use [pipx](https://github.com/pipxproject/pipx) for installing CLI tools. 

## Usage

Once installed, simply run:

```bash
$ nbhub my_cool_notebook.ipynb
```

After a couple of prompts you will receive a link [like this one](https://nbhub.duarteocarmo.com/notebook/0d856c18).

<!-- 
And here's the CLI in action:

![nbhub](https://github.com/duarteocarmo/nbhub/raw/master/assets/usage.png)
-->
## Contributing

*Note: If you want to develop new features and not sure where to start, just [email me](mailto:duarteocarmo@gmail.com).*

Start by forking this repo.

Install the development dependencies (you probably want to do this in a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/)):

```bash
 $ pip install -r requirements-dev.txt
 ```

Make sure the tests run:

```bash
 $ pytest
 ```

**Bugs and other issues** should be reported [right here](https://github.com/duarteocarmo/nbhub/issues). 

## Roadmap

- [ ] Open source the web server.
- [ ] Date limit on notebooks to be destroyed.
- [ ] Ability to set password on link creation for private notebooks.
- [ ] Improvements to CLI like only accepting notebook format.
- [ ] Web server improvements (auto clean ups, encryption, etc.)