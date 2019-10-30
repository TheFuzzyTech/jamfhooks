FROM python:3.7-stretch

LABEL Maintainer="Alex Snyder"

ENV PYTHONUNBUFFERED 1
RUN mkdir /logs
RUN mkdir /code
WORKDIR /code
RUN apt-get update
RUN apt-get -y install gcc
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["/bin/bash","entrypoint.sh"]
