#!/bin/bash

echo "Pre-release script initialized..."

LATEST_TAG=$(git describe --abbrev=0 --tags)
PROJECT_VERS=$(grep -m 1 -oP 'version = "(.*)"' pyproject.toml | sed -rn 's/.*"(.*)"/v\1/p')
INIT_VERS=$(sed -rn 's/__version__ = "(.*)"/v\1/p' ipq/__init__.py)

if [ ! $LATEST_TAG = $PROJECT_VERS ]; then
    echo "Latest tag doesn't match pyproject.toml version!"
    exit 1
elif [ ! $LATEST_TAG = $INIT_VERS ]; then
    echo "Latest tag doesn't match __init__.py version!"
    exit 1
else
    echo "$LATEST_TAG ready to release!"
fi

echo "Done!"
