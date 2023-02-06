# base image
FROM python:3.8
# setup environment variable
ENV DockerHOME=/home/app/sparking

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME