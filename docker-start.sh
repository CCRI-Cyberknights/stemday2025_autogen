#!/bin/bash
# docker-start.sh - Simple script to start the CTF with Docker

echo "🚀 Starting CCRI CTF with Docker..."

# Check if Docker is installed
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ Docker is not installed!"
    echo ""
    echo "📥 To install Docker on Ubuntu/Debian:"
    echo "   sudo apt update"
    echo "   sudo apt install docker.io docker-compose"
    echo "   sudo usermod -aG docker \$USER"
    echo "   newgrp docker"
    echo ""
    echo "📥 Or install from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if user can run docker without sudo
if ! docker ps >/dev/null 2>&1; then
    echo "⚠️ Docker requires sudo, or user not in docker group"
    echo "🔧 Run this to fix:"
    echo "   sudo usermod -aG docker \$USER"
    echo "   newgrp docker"
    echo ""
    echo "🔄 Trying with sudo for now..."
    DOCKER_CMD="sudo docker"
    if command -v docker-compose >/dev/null 2>&1; then
        COMPOSE_CMD="sudo docker-compose"
    else
        COMPOSE_CMD="sudo docker compose"
    fi
else
    DOCKER_CMD="docker"
    if command -v docker-compose >/dev/null 2>&1; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi
fi

# Check if docker-compose is available
if ! command -v docker-compose >/dev/null 2>&1 && ! $DOCKER_CMD compose version >/dev/null 2>&1; then
    echo "❌ Docker Compose is not available!"
    echo "📥 Install with: sudo apt install docker-compose"
    echo "📥 Or use newer Docker with built-in compose"
    exit 1
fi

# Build the web version first
echo "🔧 Building web version..."
cd web_version_admin/create_website
./build_web_version.sh
cd ../..

# Start with Docker Compose
echo "🐳 Starting Docker containers..."
echo "🔧 Using command: $COMPOSE_CMD"

$COMPOSE_CMD up --build -d

echo "✅ CTF is starting up..."
echo "🌐 It will be available at: http://localhost:5000"
echo "⏳ Wait about 30 seconds for everything to start..."

# Optional: Open browser automatically
sleep 5
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open http://localhost:5000
elif command -v open >/dev/null 2>&1; then
    open http://localhost:5000
fi

echo ""
echo "🛑 To stop the CTF, run: $COMPOSE_CMD down"
echo "📋 To see logs, run: $COMPOSE_CMD logs -f"