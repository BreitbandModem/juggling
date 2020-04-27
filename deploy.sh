#!/bin/bash
imageName=juggling:latest
containerName=webapp

echo Build Docker Image
docker build -t $imageName -f Dockerfile .

echo Stop and Delete old Container
docker rm -f $containerName

echo Run New Image
docker run -d \
  --privileged \
  -p 80:5000 \
  --device /dev/vchiq \
  -v $PWD/app:/usr/src/app \
  --name $containerName \
  $imageName \
  /usr/src/app/app.py
