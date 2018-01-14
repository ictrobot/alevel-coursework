#! /bin/bash

# change to project root
cd "$(dirname "$0")/.."
# delete old env quietly
rm -r env > /dev/null 2>&1
# make new virtual environment
python3 -m venv env
# activate it
source env/bin/activate
# upgrade pip, install wheel
pip install --upgrade pip wheel
# install dependencies
pip install -r requirements.txt