FROM python:3

MAINTAINER Maintainer Alex Snyder

ENV PYTHONUNBUFFERED 1
RUN mkdir /logs
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod +x entrypoint.sh
ENTRYPOINT ["bash","/code/entrypoint.sh"]
