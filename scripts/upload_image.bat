@echo off
@REM This file tags and uploads an image to Docker Hub

@REM it takes 2 arguments
@REM dockerpath is the path to upload the docker file
@REM %1 should be your dockerhub username
@REM %2 should be the name of the image to tag for upload, image should already exist in local docker installation
set dockerpath=%1/%2
 
@REM tag image for pushing
echo "Docker ID and Image: %dockerpath%"

@REM Push image to a docker repository
docker image push %dockerpath%

