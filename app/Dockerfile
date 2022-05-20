# using below base image because it is extremely lightweight, has latest stable
# Python pre-installed, and our application doesn't need many dependencies
FROM python:3.10-alpine

# add Bash so that we can execute commandline applications on a more popular and
# standard shell than the Ash shell that Alpine comes with
RUN apk update
RUN apk upgrade
RUN apk add bash

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]