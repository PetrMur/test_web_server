#!/bin/bash

HOST="0.0.0.0"
PORT="5000"
REDIS_HOST="127.0.0.1"
REDIS_PORT="6379"
REDIS_USER=""
REDIS_PASSWORD=""
MYSQL_HOST="127.0.0.1"
MYSQL_PORT="3306"
MYSQL_BASE="new_schema"
MYSQL_USER="root"
MYSQL_PASSWORD="password"
DADATA_TOKEN=""
DADATA_SECRET=""

docker stop web-service-run
docker rm web-service-run

docker run --ipc=private --pid=host --privileged --restart no \
          -e "HOST=$HOST" \
          -e "PORT=$PORT" \
          -e "MYSQL_HOST=$MYSQL_HOST" \
          -e "MYSQL_PORT=$MYSQL_PORT" \
          -e "MYSQL_BASE=$MYSQL_BASE" \
          -e "MYSQL_USER=$MYSQL_USER" \
          -e "MYSQL_PASSWORD=$MYSQL_PASSWORD" \
          -e "REDIS_HOST=$REDIS_HOST" \
          -e "REDIS_PORT=$REDIS_PORT" \
          -e "REDIS_USER=$REDIS_USER" \
          -e "REDIS_PASSWORD=$REDIS_PASSWORD" \
          -e "DADATA_SECRET=$DADATA_SECRET" \
          -e "DADATA_TOKEN=$DADATA_TOKEN" \
          # --network host \ , если локальные mysql....
          --name=web-service-run \
          -p $PORT:5000/tcp \
          -d web-service &
