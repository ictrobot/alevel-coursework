#! /bin/bash

# change to project root
cd "$(dirname "$0")/.."
# clean build directory quietly
rm -r build > /dev/null 2>&1
# activate python virtual environment
source env/bin/activate
# change to src dir
cd src
# build
pyinstaller main.py -F -w --workpath "../build/" --distpath "../build/dist/" --add-data "ngram_data/*GRAM.txt:ngram_data/"
# delete main.spec
rm main.spec 2>&1
