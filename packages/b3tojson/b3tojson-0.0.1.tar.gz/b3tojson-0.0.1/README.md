# b3tojson

This utility is intended to help converting B3 (Brasil, Bolsa, Balcão) own data format to a more portable and usable format like JSON.

## Dependencies

* jsonpickle==1.3
* requests==2.23.0

### For testing only
* pytest==5.4.1
* pytest-mock==3.0.0

## Installing

### From source

> pip install -r requirements.txt

> pip install .

### From PyPI

> pip install b3tojson

## Running

There are some configurable parameters when running in the command line. It is even possible to automatically get the latest source file and parse into a new JSON. Options are:

* `--fetch` Enables downloading of a new data file from B3 server. It will consider this file when parsing. This is disabled by default, try to parse a local file under files folder.
* `--b3_file FILENAME` Specifies the local data file location. Make sure that it is UTF-8 encoded, other encoding may not work.
* `--json_file JSONNAME` Specifies the name of the resulting JSON file. Defaults to files/stocks_data.json.

Important to note that `--fetch` and `--b3_file` are mutually exclusive.

### Example

1. Running to fetch a new file and customize the resulting JSON

> b3tojson --fetch --json_file files/beautiful_file.json

2. Using a local file to parse

> b3tojson --b3_file files/my_local_file.txt