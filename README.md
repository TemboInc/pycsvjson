pycsvjson
=========
A command-line utility to convert CSV files to JSON.

Installation
------------
**Requires:** Python 3

You should really consider using virtual environments when installing any Python software. See http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvironments-ref for more information on virtual environments.

To use virtual environments with pycsvjson, do something like:

```
pip install virtualenv
virtualenv -p $(which python3) .ve
source .ve/bin/activate
```

To install this package:
`pip install pycsvjson`

Quickstart
----------
`pycsvjson csvfile mappingfile --output outfile`

For pretty, human-readable versions of JSON, use the `--pretty` option:

`pycsvjson file.csv mapping.json --output outfile.json --pretty`

For extended options: `pycsvjson --help`

For more information on what a mapping file is, see https://github.com/pudo/jsonmapping

Status
------
This software should be considered Alpha.

License
-------
This project is released under the MIT License.
