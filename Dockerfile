# base image
FROM python:3.11.10-alpine3.20

LABEL maintainer="fellowe5@hotmail.com"

# print python output to the screen
ENV PYTHONUNBUFFERED=1

# copy requirements.txt and files in app folder to /tmp and /app directories in docker container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
# set docker containerworking directory
WORKDIR /app
# expose port 8000 of docker container
EXPOSE 8000/tcp

ARG DEV=false
# run commands in docker container
RUN \
  # create python virtual env `/py`
  python -m venv /py && \
  # upgrade pip
  /py/bin/pip install --upgrade pip && \
  # install psycopg2 dependencies
  apk add --update --no-cache postgresql-client && \
  # install psycopg2 temporary dependencies (to be removed after installing psycopg2)
  apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
  # install packages in requirements.txt
  /py/bin/pip install -r /tmp/requirements.txt && \
  # if container is built using `docker compose`, then install packages in requirements.dev.txt
  if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
  fi && \
  # remove files in `/tmp` folder
  rm -rf /tmp && \
  # remove temporary dependencies folder
  apk del .tmp-build-deps && \
  # create new non-root user
  adduser \
    --disabled-password \
    --no-create-home \
    django-user

# add python binaries to docker container system PATH environment variable
ENV PATH="/py/bin:$PATH"

# switch to django-user
USER django-user

