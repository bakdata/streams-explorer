#!/usr/bin/env bash
# from https://jaredkhan.com/blog/mypy-pre-commit

set -o errexit

# change directory to the project root directory.
cd "$(dirname "$0")"

mypy --pretty --package streams_explorer --package tests --namespace-packages
