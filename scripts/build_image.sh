#!/usr/bin/env bash
# build the image
# it takes 1 command line argument which is the tag for the image
# should be executed from the root directory of the project
docker build --tag ${1} .

# List docker images
docker image ls

# Run django project app
docker run -p 8000:80 ${1}
