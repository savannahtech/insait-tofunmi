#!/bin/bash

# Define variables
CONTAINER_NAME="question-answer-container"
IMAGE_NAME="question-answer-image"

# Stop and remove the old container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
  echo "Stopping and removing the old container..."
  docker stop $CONTAINER_NAME
  docker rm $CONTAINER_NAME
fi

# Remove the old image if it exists
if [ "$(docker images -q $IMAGE_NAME)" ]; then
  echo "Removing the old image..."
  docker rmi $IMAGE_NAME
fi

# Build the new Docker image
echo "Building the new Docker image..."
docker build -t $IMAGE_NAME .

# Run the new Docker container
echo "Starting the new container..."
docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME
