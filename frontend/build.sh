#!/bin/sh
rm -R ./build

mkdir ./build
mkdir ./build/js
cp -R ./js/vendor ./build/js

grunt

cp -R ./css/ ./build/

python ./jinja2html.py
cp *.html ./build/

cp -R ./img/ ./build/
cp -R ./fonts/ ./build/
cp ./favicon.ico ./build/
cp ./*.png ./build/