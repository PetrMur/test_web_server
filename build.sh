#!/bin/bash

docker stop web-service-run
docker rm web-service-run

docker rmi web-service
docker build --rm --no-cache --network host -f ./Dockerfile -t web-service:latest .
