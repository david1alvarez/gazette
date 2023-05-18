# gazette

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

We recommend using a python virtual environment to manage package requirements and python versions. This project is written using Python 3.11, and some features may not work with prior versions.

## Setting up your environment
### Installing Python
Python 3.11.3 can be found here: https://www.python.org/downloads/release/python-3113/

### Installing required python packages
The packages have been aggregated into the requirements.txt file at the root of the directory. Run `pip3 install -r requirements.txt`

### Using VENV
1. Set up a local virtual environment by running `python3 -m venv .venv`
2. Activate the virtual environment with `source .venv/bin/activate` (the command `deactivate` will exit the virtual environment)

## Running the server
The server can be started by running the script `start.sh`
This will ensure you your environment has the correct packages, and will start up a server at http://127.0.0.1:8000

## Using the project
The admin panel can be found at http://127.0.0.1:8000/admin/
