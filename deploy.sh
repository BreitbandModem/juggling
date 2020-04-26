#!/bin/bash
imageName=juggling:latest
containerName=webapp

echo Build Docker Image
docker build -t $imageName -f Dockerfile .

echo Stop and Delete old Container
docker rm -f $containerName

echo Run New Image
docker run -d -p 80:5000 -v $PWD/app/webapp.py:/app.py --name $containerName $imageName /app.py
