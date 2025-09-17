@echo off
REM Script to run the entire pig farm project on Windows

echo 🐷 Starting Pig Farm Project...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not installed. Please install Docker Compose.
    exit /b 1
)

REM Function to show help
if "%1"=="help" goto :show_help
if "%1"=="--help" goto :show_help
if "%1"=="-h" goto :show_help
if "%1"=="" goto :show_help

REM Main command handling
if "%1"=="up" goto :up
if "%1"=="dev" goto :dev
if "%1"=="down" goto :down
if "%1"=="build" goto :build
if "%1"=="rebuild" goto :rebuild
if "%1"=="logs" goto :logs
if "%1"=="shell" goto :shell
if "%1"=="migrate" goto :migrate
if "%1"=="superuser" goto :superuser
if "%1"=="clean" goto :clean

echo ❌ Unknown command: %1
goto :show_help

:up
echo 🚀 Starting all services...
docker-compose up -d
echo ✅ Services started!
echo 🌐 Frontend: http://localhost:8080
echo 🔧 Backend: http://localhost:8000
echo 🗄️ Database: localhost:5432
goto :end

:dev
echo 🚀 Starting development services with hot reload...
docker-compose -f docker-compose.dev.yml up -d
echo ✅ Development services started!
echo 🌐 Frontend (Hot Reload): http://localhost:8080
echo 🔧 Backend: http://localhost:8000
echo 🗄️ Database: localhost:5433
goto :end

:down
echo 🛑 Stopping all services...
docker-compose down
echo ✅ Services stopped!
goto :end

:build
echo 🔨 Building all images...
docker-compose build
echo ✅ Build completed!
goto :end

:rebuild
echo 🔄 Rebuilding and starting all services...
docker-compose down
docker-compose build --no-cache
docker-compose up -d
echo ✅ Rebuild completed!
goto :end

:logs
echo 📋 Showing logs...
docker-compose logs -f
goto :end

:shell
echo 🐚 Opening shell in backend container...
docker-compose exec backend bash
goto :end

:migrate
echo 🔄 Running Django migrations...
docker-compose exec backend python manage.py migrate
echo ✅ Migrations completed!
goto :end

:superuser
echo 👤 Creating Django superuser...
docker-compose exec backend python manage.py createsuperuser
goto :end

:clean
echo 🧹 Cleaning up containers and volumes...
docker-compose down -v
docker system prune -f
echo ✅ Cleanup completed!
goto :end

:show_help
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   up          Start all services
echo   dev         Start development services with hot reload
echo   down        Stop all services
echo   build       Build all images
echo   rebuild     Rebuild and start all services
echo   logs        Show logs for all services
echo   shell       Open shell in backend container
echo   migrate     Run Django migrations
echo   superuser   Create Django superuser
echo   clean       Clean up containers and volumes
echo   help        Show this help message
goto :end

:end