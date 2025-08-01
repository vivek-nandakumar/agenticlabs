#!/bin/bash

# SRE Agent Deployment Script
# This script helps deploy the SRE AI Agent in different environments

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="sre-agent"
DEFAULT_ENVIRONMENT="stage"

# Functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  SRE Agent Deployment Script${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_step() {
    echo -e "${YELLOW}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

check_prerequisites() {
    print_step "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Python is installed (for local development)
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 is not installed. Local development mode will not be available."
    fi
    
    print_success "Prerequisites check completed"
}

check_environment_variables() {
    print_step "Checking environment variables..."
    
    # Check for OpenAI API key
    if [ -z "$OPENAI_API_KEY" ]; then
        print_error "OPENAI_API_KEY environment variable is not set."
        echo "Please set it with: export OPENAI_API_KEY='your-api-key'"
        exit 1
    fi
    
    # Set default environment if not specified
    if [ -z "$ENVIRONMENT" ]; then
        ENVIRONMENT=$DEFAULT_ENVIRONMENT
        print_info "Using default environment: $ENVIRONMENT"
    fi
    
    print_success "Environment variables check completed"
}

build_docker_image() {
    print_step "Building Docker image..."
    
    cd "$SCRIPT_DIR"
    
    if docker build -t "$PROJECT_NAME" .; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

deploy_with_docker_compose() {
    print_step "Deploying with Docker Compose..."
    
    cd "$SCRIPT_DIR"
    
    # Stop existing containers
    print_info "Stopping existing containers..."
    docker-compose down --remove-orphans
    
    # Start services
    print_info "Starting services..."
    if docker-compose up -d; then
        print_success "Services started successfully"
    else
        print_error "Failed to start services"
        exit 1
    fi
    
    # Wait for services to be ready
    print_info "Waiting for services to be ready..."
    sleep 30
    
    # Check service health
    check_service_health
}

check_service_health() {
    print_step "Checking service health..."
    
    # Check SRE Agent API
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "SRE Agent API is healthy"
    else
        print_error "SRE Agent API is not responding"
        return 1
    fi
    
    # Check Grafana (if enabled)
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        print_success "Grafana is accessible"
    else
        print_warning "Grafana is not accessible (may still be starting)"
    fi
    
    # Check Prometheus (if enabled)
    if curl -f http://localhost:9090 > /dev/null 2>&1; then
        print_success "Prometheus is accessible"
    else
        print_warning "Prometheus is not accessible (may still be starting)"
    fi
}

deploy_local() {
    print_step "Deploying locally (without Docker)..."
    
    cd "$SCRIPT_DIR"
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv .venv
    fi
    
    # Activate virtual environment
    print_info "Activating virtual environment..."
    source .venv/bin/activate
    
    # Install dependencies
    print_info "Installing dependencies..."
    pip install -r requirements.txt
    
    # Run the agent
    print_info "Starting SRE Agent..."
    python sre_agent_api.py &
    
    # Wait for service to start
    sleep 10
    
    # Check health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "SRE Agent is running locally"
    else
        print_error "SRE Agent failed to start"
        exit 1
    fi
}

show_status() {
    print_step "Service Status"
    
    echo ""
    echo "Service URLs:"
    echo "  SRE Agent API:     http://localhost:8000"
    echo "  API Documentation: http://localhost:8000/docs"
    echo "  Health Check:      http://localhost:8000/health"
    echo "  Grafana:           http://localhost:3000 (admin/admin)"
    echo "  Prometheus:        http://localhost:9090"
    echo "  Kibana:            http://localhost:5601"
    echo ""
    
    # Show running containers
    echo "Running containers:"
    docker-compose ps
}

show_logs() {
    print_step "Recent logs"
    docker-compose logs --tail=50
}

stop_services() {
    print_step "Stopping services..."
    cd "$SCRIPT_DIR"
    docker-compose down
    print_success "Services stopped"
}

cleanup() {
    print_step "Cleaning up..."
    cd "$SCRIPT_DIR"
    
    # Stop and remove containers
    docker-compose down --volumes --remove-orphans
    
    # Remove images
    docker rmi "$PROJECT_NAME" 2>/dev/null || true
    
    print_success "Cleanup completed"
}

show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy          Deploy the SRE Agent (default)"
    echo "  deploy:local    Deploy locally without Docker"
    echo "  status          Show service status"
    echo "  logs            Show recent logs"
    echo "  stop            Stop all services"
    echo "  cleanup         Stop services and clean up Docker resources"
    echo "  help            Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  OPENAI_API_KEY  Your OpenAI API key (required)"
    echo "  ENVIRONMENT     Environment to deploy (dev/stage, default: stage)"
    echo ""
    echo "Examples:"
    echo "  $0 deploy"
    echo "  ENVIRONMENT=dev $0 deploy"
    echo "  $0 status"
}

# Main script
main() {
    print_header
    
    # Parse command line arguments
    COMMAND=${1:-deploy}
    
    case $COMMAND in
        "deploy")
            check_prerequisites
            check_environment_variables
            build_docker_image
            deploy_with_docker_compose
            show_status
            ;;
        "deploy:local")
            check_prerequisites
            check_environment_variables
            deploy_local
            show_status
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "stop")
            stop_services
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $COMMAND"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 