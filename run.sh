#!/bin/bash

# 사용법: ./run.sh [up|down|logs|build]

COMMAND=$1

case $COMMAND in
  up)
    echo "Starting Spark cluster in detached mode..."
    docker-compose up -d
    ;;
  down)
    echo "Stopping Spark cluster..."
    docker-compose down
    ;;
  logs)
    SERVICE=$2
    if [ -z "$SERVICE" ]; then
      echo "Following logs from all services..."
      docker-compose logs -f
    else
      echo "Following logs from $SERVICE..."
      docker-compose logs -f $SERVICE
    fi
    ;;
  build)
    echo "Forcing a rebuild of the Docker images..."
    docker-compose build --no-cache
    ;;
  *)
    echo "Usage: $0 {up|down|logs [service_name]|build}"
    exit 1
    ;;
esac
