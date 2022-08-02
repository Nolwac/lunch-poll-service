@echo off
@REM build the image
@REM it takes 1 command line argument which is the tag for the image
@REM should be executed from the root directory of the project
docker build --tag %1 .

@REM List docker images
docker image ls

@REM Run django project app
docker run -p 8000:80 %1
