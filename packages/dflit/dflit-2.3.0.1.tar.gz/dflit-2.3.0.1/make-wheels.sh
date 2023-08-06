#!/bin/sh

cur=$(pwd)

export PYTHONPATH=${cur}:${cur}/flit_core
export SOURCE_DATE_EPOCH=$(git show -s --format=%ct HEAD)

git show -s --format='%C(cyan)committer date of HEAD: %ci%C(reset)' HEAD
echo "PYTHONPATH=$PYTHONPATH"
echo "SOURCE_DATE_EPOCH=$SOURCE_DATE_EPOCH"

set -x
python -m pep517.build -o ../dist flit_core
python -m flit build
