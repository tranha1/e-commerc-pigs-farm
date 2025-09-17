#!/bin/bash

# Script to run the entire pig farm project

echo "🐷 Starting Pig Farm Project..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install Docker Compose."
    exit 1
fi

# Function to show help
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  up          Start all services"
    echo "  dev         Start development services with hot reload"
    echo "  down        Stop all services"
    echo "  build       Build all images"
    echo "  rebuild     Rebuild and start all services"
    echo "  logs        Show logs for all services"
    echo "  shell       Open shell in backend container"
    echo "  migrate     Run Django migrations"
    echo "  superuser   Create Django superuser"
    echo "  clean       Clean up containers and volumes"
    echo "  help        Show this help message"
}

# Main command handling
case "$1" in
    "up")
        echo "🚀 Starting all services..."
        docker-compose up -d
        echo "✅ Services started!"
        echo "🌐 Frontend: http://localhost:8080"
        echo "🔧 Backend: http://localhost:8000"
        echo "🗄️ Database: localhost:5432"
        ;;
    "dev")
        echo "🚀 Starting development services with hot reload..."
        docker-compose -f docker-compose.dev.yml up -d
        echo "✅ Development services started!"
        echo "🌐 Frontend (Hot Reload): http://localhost:8080"
        echo "🔧 Backend: http://localhost:8000"
        echo "🗄️ Database: localhost:5433"
        ;;
    "down")
        echo "🛑 Stopping all services..."
        docker-compose down
        echo "✅ Services stopped!"
        ;;
    "build")
        echo "🔨 Building all images..."
        docker-compose build
        echo "✅ Build completed!"
        ;;
    "rebuild")
        echo "🔄 Rebuilding and starting all services..."
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        echo "✅ Rebuild completed!"
        ;;
    "logs")
        echo "📋 Showing logs..."
        docker-compose logs -f
        ;;
    "shell")
        echo "🐚 Opening shell in backend container..."
        docker-compose exec backend /bin/bash
        ;;
    "migrate")
        echo "🔄 Running Django migrations..."
        docker-compose exec backend python manage.py migrate
        echo "✅ Migrations completed!"
        ;;
    "superuser")
        echo "👤 Creating Django superuser..."
        docker-compose exec backend python manage.py createsuperuser
        ;;
    "clean")
        echo "🧹 Cleaning up containers and volumes..."
        docker-compose down -v
        docker system prune -f
        echo "✅ Cleanup completed!"
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_help
        exit 1
        ;;
esac