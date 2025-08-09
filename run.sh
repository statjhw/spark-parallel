#!/bin/bash

# Spark Parallel Processing Management Script
# Usage: ./run.sh [command] [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Check required files
check_requirements() {
    if [ ! -f ".env" ]; then
        print_error "Missing .env file. Please create it with required environment variables."
        exit 1
    fi
    
    if [ ! -f ".secrets/service_account.json" ]; then
        print_error "Missing service account file at .secrets/service_account.json"
        exit 1
    fi
    
    if [ ! -d "jars" ] || [ -z "$(ls -A jars/ 2>/dev/null)" ]; then
        print_warning "jars/ directory is empty. Make sure to download required JAR files."
    fi
}

# Build the Docker image
build_image() {
    print_status "Building Spark Docker image..."
    docker build -f docker/spark/Dockerfile -t spark-parallel:latest .
    print_status "Docker image built successfully!"
}

# Start services
start_services() {
    check_docker
    check_requirements
    
    print_status "Starting Spark cluster..."
    
    # Build image if it doesn't exist
    if ! docker image inspect spark-parallel:latest >/dev/null 2>&1; then
        print_status "Image not found. Building..."
        build_image
    fi
    
    docker-compose up -d
    
    print_status "Spark cluster started!"
    print_status "Web UIs available at:"
    print_status "  - Spark Master: http://localhost:8080"
    print_status "  - Worker 1: http://localhost:8081"
    print_status "  - Worker 2: http://localhost:8082"
}

# Stop services
stop_services() {
    print_status "Stopping Spark cluster..."
    docker-compose down
    print_status "Spark cluster stopped!"
}

# Show logs
show_logs() {
    if [ -n "$2" ]; then
        docker-compose logs -f "$2"
    else
        docker-compose logs -f
    fi
}

# Show status
show_status() {
    docker-compose ps
}

# Clean up (remove containers and images)
cleanup() {
    print_warning "This will remove all containers and the Docker image."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleaning up..."
        docker-compose down -v --remove-orphans
        docker image rm spark-parallel:latest 2>/dev/null || true
        print_status "Cleanup complete!"
    fi
}

# Show help
show_help() {
    echo "Spark Parallel Processing Management Script"
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  up, start     Start the Spark cluster"
    echo "  down, stop    Stop the Spark cluster"
    echo "  restart       Restart the Spark cluster"
    echo "  build         Build the Docker image"
    echo "  logs [service] Show logs (optionally for specific service)"
    echo "  status, ps    Show container status"
    echo "  cleanup       Remove containers and images"
    echo "  help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 up"
    echo "  $0 logs spark-master"
    echo "  $0 down"
    echo ""
    echo "Services: spark-master, spark-worker-1, spark-worker-2, spark-app"
}

# Main command handling
case "$1" in
    "up"|"start")
        start_services
        ;;
    "down"|"stop")
        stop_services
        ;;
    "restart")
        stop_services
        start_services
        ;;
    "build")
        check_docker
        build_image
        ;;
    "logs")
        show_logs "$@"
        ;;
    "status"|"ps")
        show_status
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"--help"|"-h"|"")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
