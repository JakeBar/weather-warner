#!/bin/bash

# Break out if there's an error
set -e

# Clean up & remove old containers
echo "🛑  Taking down containers..."
docker-compose down -v
echo "🚿  Clearing out old containers..."
docker-compose kill
docker-compose rm -fv

# Build App
echo "🏗️  Building new containers..."
docker-compose build django

# Run Migrations
echo "🗄️  Migrating database..."
docker-compose run --rm django ./manage.py migrate

docker-compose up -d django
echo "Server is now running 👟 at http://0.0.0.0:8000/"
