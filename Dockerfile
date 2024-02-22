# syntax=docker/dockerfile:1
# TODO при создании контейнера файл выложить в корневой каталог, туда же выложить requirements.txt

FROM python:3.9-alpine
RUN mkdir /sea_battle
WORKDIR /sea_battle

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY .. .

WORKDIR src

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:5000


