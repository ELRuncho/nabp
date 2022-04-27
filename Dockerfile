FROM python:latest

WORKDIR /app

COPY . .

RUN pip3 install aws-cli

RUN pip3 install .

