# weather-warner
Simple Weather Notifications via Text (SMS)

[![CircleCI](https://circleci.com/gh/JakeBar/weather-warner.svg?style=svg&circle-token=44b5a718bad263f1082e56881233f23ec3cc3165)](https://circleci.com/gh/JakeBar/weather-warner)

## Requirements

* Docker Compose
* Docker

Note: For Mac users, I recommend [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/), as it includes both.

## Setup

1. Run `./dev_setup.sh` to install the dockerised application.

### Developer Tools

#### Tests

Run `./shortcuts.sh test` to start pytests.

Note: You can debug tests by inserting a breakpoint (_see Debugging_) and running:
```
./shortcuts.sh test --capture=no --pdb --pdbcls=IPython.terminal.debugger:Pdb--capture=no --pdb --pdbcls=IPython.terminal.debugger:Pdb
```

#### Linting

This code uses pre-commit to enforce coding style locally. Ensure you have Python 3.7 if you'd like to run linting.

Run `./shortcuts.sh lint` to lint changed files.
