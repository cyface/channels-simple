#!/usr/bin/env bash
eval "$(docker-machine env default)"
docker-compose stop nginx
docker-compose kill -s SIGINT workerserver
docker-compose stop db redis
sleep 1s
docker-compose up -d