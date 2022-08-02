#!/usr/bin/env bash
# This file tags and uploads an image to Docker Hub

# it takes 2 arguments
# dockerpath is the path to upload the docker file
# $1 should be your dockerhub username
# $2 should be the name of the image to tag for upload, image should already exist in local docker installation
dockerpath=${1}/${2}
 
# tag image for pushing
docker image tag ${2} $dockerpath
echo "Docker ID and Image: $dockerpath"

# Push image to a docker repository
docker image push $dockerpath

