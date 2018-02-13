#!/bin/sh
set -e
export FLASK_ENV="TESTING"
coverage run -m nose "$@"
coverage report -m
