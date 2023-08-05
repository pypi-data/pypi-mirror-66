#!/bin/bash
cd $(git rev-parse --show-toplevel)
set -e

BUILD=1 ./bin/test.sh

rm -rf dist build *.egg-info
python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# echo 'to prod? (press enter)'; read;
python3 -m twine upload dist/*
git push --tags
