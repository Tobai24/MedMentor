#!/bin/bash

# code to build and stop the docker image
if [ "$1" == "stop" ]; then
    docker compose down
    echo "Docker Compose has been stopped!"
else
    #build docker image for the docker-compose
    docker build -t rag_pipeline .
    docker compose up
    echo "Docker Compose is now running!"
fi