#!/usr/bin/env bash
eval "$(docker-machine env default)"
docker-compose stop nginx
docker-compose stop interfaceserver
docker-compose stop workerserver_1
docker-compose stop workerserver_2
docker-compose stop db redis
sleep 1s
docker-compose up -d