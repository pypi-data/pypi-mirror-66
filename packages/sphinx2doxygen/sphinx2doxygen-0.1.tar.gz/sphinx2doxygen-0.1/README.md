# sphinx2doxygen
is a simple documentation string parser. It's aim is to rewrite [Sphinx](https://thomas-cokelaer.info/tutorials/sphinx/index.html) style documentation strings to 
[Google](https://google.github.io/styleguide/pyguide.html) style documentation strings that are compatible with [Doxygen](http://www.doxygen.nl/).
## Installation
```
pip install pep2google
```

## Usage
```
sphinx2doxygen [-h] [-f] -i DIR -o DIR [-e expr]

Rewrites python docstring code commenting from PEP to Google style.

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           do not ask before overwriting files
  -i DIR, --input-dir DIR
                        source code directory
  -o DIR, --output-dir DIR
                        directory for the rewritten files
  -e expr, --expression expr
                        only process files that match the given expression (default: *.py)
```

### Bugs
Please open a ticket in the [issue tracker](https://github.com/br-olf/sphinx2doxygen/issues).

