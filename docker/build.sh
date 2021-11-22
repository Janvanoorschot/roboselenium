#!/usr/bin/env bash

# get the root directory
CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
DIR="$(dirname "$CURDIR")"
export DOCKERDIR=$DIR/docker

# spec the current version
VERSION=1.0

# create the docker images
cd $DOCKERDIR
docker build -f $DOCKERDIR/Dockerfile -t robomind/roboselenium:$VERSION .
