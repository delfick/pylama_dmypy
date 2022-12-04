#!/bin/bash

# Bash does not make it easy to find where this file is
# Here I'm making it so it doesn't matter what directory you are in
# when you execute this script. And it doesn't matter whether you're
# executing a symlink to this script
# Note the `-h` in the while loop asks if this path is a symlink
pushd . >'/dev/null'
SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
while [ -h "$SCRIPT_PATH" ]; do
    cd "$(dirname -- "$SCRIPT_PATH")"
    SCRIPT_PATH="$(readlink -f -- "$SCRIPT_PATH")"
done
cd "$(dirname -- "$SCRIPT_PATH")" >'/dev/null'

# Now we get to the script itself!
HANDLED=0
if [[ "$#" == "1" ]]; then
    # Special case activate to make the virtualenv active in this session
    if [[ "$1" == "activate" ]]; then
        if [[ "$0" = "$BASH_SOURCE" ]]; then
            echo "You need to run as 'source ./run.sh $1'"
            exit 1
        fi
        VENVSTARTER_ONLY_MAKE_VENV=1 ./tools/venv

        if [[ "$1" == "activate" ]]; then
            source ./tools/.python/bin/activate
            HANDLED=1
        fi
    fi
fi

if [[ $HANDLED != 1 ]]; then
    exec ./tools/venv "$@"
fi