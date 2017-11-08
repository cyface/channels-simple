#!/usr/bin/env bash
docker-compose run workerserver python manage.py migrate --noinput --settings=channels_simple.settings_docker_compose
docker-compose run workerserver python manage.py collectstatic --noinput --settings=channels_simple.settings_docker_compose
docker-compose run workerserver python manage.py createsuperuser --settings=channels_simple.settings_docker_compose