#!/bin/sh
set -e
export FLASK_ENV="TESTING"
if [ $# -eq 0 ]; then
    pytest --cov=baseframe
else
    pytest "$@"
fi
