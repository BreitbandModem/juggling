#!/bin/bash

DEBUG=0

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -d|--debug)
    DEBUG=1
    shift # past argument
    shift # past value
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

imageName=juggling:latest
containerName=webapp

echo Build Docker Image
docker build -t $imageName -f Dockerfile .

echo Stop and Delete old Container
docker rm -f $containerName

echo Run New Image
if [ $DEBUG -eq 0 ]; then
  docker run -d \
    --privileged \
    -p 80:5000 \
    --device /dev/vchiq \
    -v $PWD/app:/usr/src/app \
    -v $PWD/logs:/logs \
    -v $PWD/videos/out \
    --name $containerName \
    $imageName \
    /usr/src/app/app.py
else
  docker run --rm \
    --privileged \
    -p 80:5000 \
    --device /dev/vchiq \
    -v $PWD/app:/usr/src/app \
    -v $PWD/logs:/logs \
    -v $PWD/videos/out \
    --name $containerName \
    $imageName \
    /usr/src/app/app.py
fi
