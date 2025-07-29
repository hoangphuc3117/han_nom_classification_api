#!/bin/bash

# Quick Docker Setup Script for Han Nom Classification API
# Usage: ./quick-docker.sh [dev|prod|clean|status]

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project variables
PROJECT_NAME="han-nom-classification-api"
API_PORT=8000
DEV_PORT=8001

print_help() {
    echo -e "${BLUE}Han Nom Classification API - Quick Docker Setup${NC}"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo -e "  ${GREEN}dev${NC}     - Start development environment with hot reload"
    echo -e "  ${GREEN}prod${NC}    - Start production environment"
    echo -e "  ${GREEN}nginx${NC}   - Start production with nginx reverse proxy"
    echo -e "  ${GREEN}clean${NC}   - Stop and clean up all containers"
    echo -e "  ${GREEN}status${NC}  - Show status of containers"
    echo -e "  ${GREEN}logs${NC}    - Show logs from running containers"
    echo -e "  ${GREEN}shell${NC}   - Open shell in running container"
    echo -e "  ${GREEN}test${NC}    - Run tests in container"
    echo ""
}

check_requirements() {
    echo -e "${YELLOW}Checking requirements...${NC}"
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
        exit 1
    fi
    
    # Check if Docker Compose is available
    if ! docker compose version &> /dev/null && ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose is not available. Please install Docker Compose.${NC}"
        exit 1
    fi
    
    # Check if models directory exists
    if [ ! -d "./models" ]; then
        echo -e "${YELLOW}⚠️  Models directory not found. Creating it...${NC}"
        mkdir -p ./models
        echo -e "${YELLOW}Please ensure your model files are in the ./models directory${NC}"
    fi
    
    echo -e "${GREEN}✅ Requirements check passed${NC}"
}

start_dev() {
    echo -e "${GREEN}🚀 Starting development environment...${NC}"
    check_requirements
    
    # Build and start development container
    docker compose --profile dev up -d --build
    
    echo -e "${GREEN}✅ Development environment started!${NC}"
    echo -e "${BLUE}📖 API Documentation: http://localhost:${DEV_PORT}/docs${NC}"
    echo -e "${BLUE}🔄 Hot reload is enabled - changes will be reflected automatically${NC}"
}

start_prod() {
    echo -e "${GREEN}🚀 Starting production environment...${NC}"
    check_requirements
    
    # Build and start production container
    docker compose up -d --build han-nom-api
    
    echo -e "${GREEN}✅ Production environment started!${NC}"
    echo -e "${BLUE}📖 API Documentation: http://localhost:${API_PORT}/docs${NC}"
}

start_nginx() {
    echo -e "${GREEN}🚀 Starting production environment with nginx...${NC}"
    check_requirements
    
    # Build and start production with nginx
    docker compose --profile production up -d --build
    
    echo -e "${GREEN}✅ Production environment with nginx started!${NC}"
    echo -e "${BLUE}📖 API Documentation: http://localhost/docs${NC}"
    echo -e "${BLUE}🌐 API available through nginx reverse proxy${NC}"
}

clean_containers() {
    echo -e "${YELLOW}🧹 Cleaning up containers and images...${NC}"
    
    # Stop all containers
    docker compose down --remove-orphans
    
    # Remove project images
    docker images | grep "$PROJECT_NAME" | awk '{print $3}' | xargs -r docker rmi -f
    
    # Clean up unused resources
    docker system prune -f
    
    echo -e "${GREEN}✅ Cleanup completed!${NC}"
}

show_status() {
    echo -e "${BLUE}📊 Container Status:${NC}"
    echo ""
    
    # Show running containers
    docker ps --filter "name=han-nom" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo ""
    echo -e "${BLUE}🖼️  Images:${NC}"
    docker images | grep -E "(han-nom|nginx)" || echo "No project images found"
    
    echo ""
    echo -e "${BLUE}🔗 Service URLs:${NC}"
    if docker ps | grep -q "han-nom-api-dev"; then
        echo -e "  Development API: ${GREEN}http://localhost:${DEV_PORT}/docs${NC}"
    fi
    if docker ps | grep -q "han-nom-api" && ! docker ps | grep -q "nginx"; then
        echo -e "  Production API: ${GREEN}http://localhost:${API_PORT}/docs${NC}"
    fi
    if docker ps | grep -q "nginx"; then
        echo -e "  Production API (nginx): ${GREEN}http://localhost/docs${NC}"
    fi
}

show_logs() {
    echo -e "${BLUE}📋 Container Logs:${NC}"
    docker compose logs -f --tail=50
}

open_shell() {
    echo -e "${BLUE}🐚 Opening shell in container...${NC}"
    
    # Try to find running container
    if docker ps | grep -q "han-nom-api-dev"; then
        docker exec -it han-nom-classification-api-han-nom-api-dev-1 /bin/bash
    elif docker ps | grep -q "han-nom-api"; then
        docker exec -it han-nom-classification-api-han-nom-api-1 /bin/bash
    else
        echo -e "${RED}❌ No running containers found${NC}"
        exit 1
    fi
}

run_tests() {
    echo -e "${BLUE}🧪 Running tests...${NC}"
    check_requirements
    
    # Build development image and run tests
    docker compose -f docker-compose.yml run --rm han-nom-api-dev pytest tests/ -v
    
    echo -e "${GREEN}✅ Tests completed!${NC}"
}

# Main script logic
case "${1:-help}" in
    "dev")
        start_dev
        ;;
    "prod")
        start_prod
        ;;
    "nginx")
        start_nginx
        ;;
    "clean")
        clean_containers
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    "shell")
        open_shell
        ;;
    "test")
        run_tests
        ;;
    "help"|*)
        print_help
        ;;
esac