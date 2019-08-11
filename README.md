# weather-warner
Simple Weather Notifications via Text (SMS) - weatherwarner.herokuapp.com

[![CircleCI](https://circleci.com/gh/JakeBar/weather-warner.svg?style=svg&circle-token=44b5a718bad263f1082e56881233f23ec3cc3165)](https://circleci.com/gh/JakeBar/weather-warner)

## Features

* Weather Warner sends a short weather update via SMS. Updates are sent each morning based on the current day's forecast data.
* Recipients can subscribe to texts at weatherwarner.herokuapp.com after verifying their number.
* Current recipients can be managed via the [admin page](weatherwarner.herokuapp.com/admin).

## Requirements

* Docker Compose
* Docker

Note: For Mac users, I recommend [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/), as it includes both.

## Setup

1. Run `./dev_setup.sh` to install the dockerised application. This will install everything required and import fixtures.

## Usage

1. Start Docker Compose
2. Configure the Twilio Variables (`TWILIO_*` in `base.py`) with production credentials
3. Configure the Weather Bit `API_KEY` with a production key
3. In the base directory, run `./shortcuts.sh send_weather_report` to fire off the texts!

## System Architecture

### Backend

The application backend is built with an python web framework called [Django](https://en.wikipedia.org/wiki/Django_(web_framework)) backed by a PostgreSQL database. Django's ORM is powerful, so we're going to make the most of that!


Two third party APIs are used; [Weatherbit](https://www.weatherbit.io/api) for retrieving weather data and [Twilio Programmable SMS](https://www.twilio.com/docs/sms) to send and receive texts.

### Frontend

The application frontend is a React/Typescript node app using React Hooks & Axios. A static webpack build is generated during deployment and served to the backend via django-webpack-loader.


### Infrastructure

The application is contained within [Docker](https://en.wikipedia.org/wiki/Docker_(software)) using [Docker Compose](https://docs.docker.com/compose/).

[Circle CI](https://circleci.com/) is used for continuous integration to run linting & tests.

When CI passes, the application is automatically deployed to heroku using [multiple buildpacks](https://devblog.kogan.com/blog/making-heroku-subdirectories-easier).

### Developer Tools

#### Running Locally

The webserver and webpack are required to run locally. Use the following commands:

```
dc up -d django
yarn run start
```

#### Tests

##### Backend

1. Run `./shortcuts.sh test` to start pytests.

Note: You can debug tests by inserting a breakpoint (_see Debugging_) and running:
```
./shortcuts.sh test --capture=no --pdb --pdbcls=IPython.terminal.debugger:Pdb--capture=no --pdb --pdbcls=IPython.terminal.debugger:Pdb
```

##### Frontend

1. Run `yarn run test` from the `frontend/` root directory to run the frontend test suite.

#### Linting

This code uses pre-commit to enforce coding style locally. Ensure you have Python 3.7 if you'd like to run linting.

Run `./shortcuts.sh lint` to lint changed files.

#### Application Shortcuts

`./shorcuts.sh` can be run for a variety of custom commands.

Available subcommands:

    logs:   Follow the logs for the django container
    shell:  Open a shell_plus session
    bash:   Start a bash session in the app container
    test:   Run one or more tests
    lint:   Run isort, flake8 and black on changed files

#### Debugging

Insert a breakpoint in the application like so:

```
foo = "bar"
import ipdb ; ipdb.set_trace() <=== break point
print(foo)
```
