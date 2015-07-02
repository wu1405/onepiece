FROM python:2.7
MAINTAINER songjiao@cyou-inc.com
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y  libldap2-dev libsasl2-dev vim
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD entrypoint.sh /