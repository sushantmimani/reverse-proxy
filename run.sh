#!/usr/bin/env bash


control_c()
# run if user hits control-c
{
  echo "Bring down service and freeing up associated volumes"
  docker-compose down -v
}

trap control_c SIGINT

docker-compose up

