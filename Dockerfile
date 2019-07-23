FROM python:3.7

RUN apt update \
    && groupadd -r django \
    && useradd -r --uid 1000 --create-home -g django django

ENV PYTHONUNBUFFERED 1

RUN pip install -U pip && pip install pipenv

COPY ./Pipfile* /

RUN pipenv install --system --dev

RUN mkdir /app

USER django

WORKDIR /app
