# using below base image because it is extremely lightweight, has latest stable
# Python pre-installed, and our application doesn't need many dependencies
FROM python:3.10-alpine

# add Bash so that we can execute commandline applications on a more popular and
# standard shell than the Ash shell that Alpine comes with
RUN apk update
RUN apk upgrade
RUN apk add bash

WORKDIR /application

COPY . .

# TODO:
# port/expose stuff...

# TODO:
# run application server...