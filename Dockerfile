FROM python:latest

WORKDIR /app

COPY . .

RUN pip3 install aws-cli -y

RUN pip3 install .

