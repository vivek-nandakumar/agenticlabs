#!/bin/bash

# SRE AI Agent Deployment Script - Final Architecture
# This script deploys the complete SRE AI Agent with all components

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="sre-ai-agent"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Function to create environment file
create_env_file() {
    print_status "Creating environment file..."
    
    if [ ! -f "$ENV_FILE" ]; then
        cat > "$ENV_FILE" << EOF
# SRE AI Agent Environment Configuration
# Final Architecture with JWT, mTLS, and OTLP

# Security Configuration
JWT_SECRET=$(openssl rand -hex 32)
NEXTAUTH_SECRET=$(openssl rand -hex 32)

# Database Configuration
POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres
POSTGRES_DB=sre_agent_db

# Redis Configuration
REDIS_URL=redis://redis:6379

# Model Configuration
MODEL_URL=http://ollama:11434
MODEL_NAME=llama3.1:8b

# Observability Configuration
OTLP_ENDPOINT=http://otel-collector:4317
LANGFUSE_ENDPOINT=http://langfuse:3000

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Dashboard Configuration
DASHBOARD_PORT=8501

# Monitoring Configuration
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
JAEGER_PORT=16686

# Logging Configuration
LOG_LEVEL=INFO
EOF
        print_success "Environment file created"
    else
        print_warning "Environment file already exists"
    fi
}

# Function to create SSL certificates for mTLS
create_ssl_certs() {
    print_status "Creating SSL certificates for mTLS..."
    
    mkdir -p certs
    
    # Generate CA certificate
    openssl req -x509 -newkey rsa:4096 -keyout certs/ca.key -out certs/ca.crt -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=SRE-Agent-CA"
    
    # Generate server certificate
    openssl req -newkey rsa:4096 -keyout certs/server.key -out certs/server.csr -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=sre-agent-server"
    openssl x509 -req -in certs/server.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial \
        -out certs/server.crt -days 365
    
    # Generate client certificate
    openssl req -newkey rsa:4096 -keyout certs/client.key -out certs/client.csr -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=sre-agent-client"
    openssl x509 -req -in certs/client.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial \
        -out certs/client.crt -days 365
    
    # Set proper permissions
    chmod 600 certs/*.key
    chmod 644 certs/*.crt
    
    print_success "SSL certificates created"
}

# Function to initialize database
init_database() {
    print_status "Initializing database..."
    
    # Create init.sql for PostgreSQL
    cat > init.sql << EOF
-- Initialize SRE Agent Database
CREATE DATABASE IF NOT EXISTS sre_agent_db;
CREATE DATABASE IF NOT EXISTS langfuse;

-- Create tables for SRE monitoring data
\c sre_agent_db;

CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    disk_usage DECIMAL(5,2),
    network_latency DECIMAL(10,2),
    service_name VARCHAR(100),
    environment VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    alert_name VARCHAR(200),
    severity VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    service_name VARCHAR(100),
    environment VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    incident_id VARCHAR(50),
    title VARCHAR(200),
    description TEXT,
    severity VARCHAR(20),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    assigned_to VARCHAR(100),
    service_name VARCHAR(100),
    environment VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    service_name VARCHAR(100),
    endpoint VARCHAR(200),
    response_time DECIMAL(10,2),
    error_rate DECIMAL(5,2),
    throughput DECIMAL(10,2),
    environment VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS automated_actions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    action_type VARCHAR(100),
    description TEXT,
    status VARCHAR(20),
    incident_id VARCHAR(50),
    service_name VARCHAR(100),
    environment VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS jira_tickets (
    id SERIAL PRIMARY KEY,
    ticket_id VARCHAR(50),
    title VARCHAR(200),
    description TEXT,
    priority VARCHAR(20),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    assignee VARCHAR(100),
    incident_id VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS slack_channels (
    id SERIAL PRIMARY KEY,
    channel_name VARCHAR(100),
    channel_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    incident_id VARCHAR(50),
    status VARCHAR(20)
);
EOF
    
    print_success "Database initialization script created"
}

# Function to create monitoring directories
create_monitoring_dirs() {
    print_status "Creating monitoring directories..."
    
    mkdir -p monitoring/grafana/dashboards
    mkdir -p monitoring/grafana/datasources
    mkdir -p monitoring/vanguard
    
    # Create Grafana datasource configuration
    cat > monitoring/grafana/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF
    
    # Create basic Grafana dashboard
    cat > monitoring/grafana/dashboards/sre-agent-dashboard.json << EOF
{
  "dashboard": {
    "id": null,
    "title": "SRE Agent Dashboard",
    "tags": ["sre", "monitoring"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "System Health",
        "type": "stat",
        "targets": [
          {
            "expr": "up",
            "refId": "A"
          }
        ]
      }
    ]
  }
}
EOF
    
    print_success "Monitoring directories created"
}

# Function to build and start services
deploy_services() {
    print_status "Building and starting services..."
    
    # Pull latest images
    docker-compose pull
    
    # Build the SRE agent image
    docker-compose build sre-agent
    
    # Start all services
    docker-compose up -d
    
    print_success "Services deployed successfully"
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for PostgreSQL
    print_status "Waiting for PostgreSQL..."
    until docker-compose exec -T postgres pg_isready -U postgres; do
        sleep 2
    done
    
    # Wait for Redis
    print_status "Waiting for Redis..."
    until docker-compose exec -T redis redis-cli ping; do
        sleep 2
    done
    
    # Wait for Ollama
    print_status "Waiting for Ollama..."
    until curl -f http://localhost:11434/api/tags; do
        sleep 5
    done
    
    # Wait for SRE Agent API
    print_status "Waiting for SRE Agent API..."
    until curl -f http://localhost:8000/health; do
        sleep 5
    done
    
    print_success "All services are ready"
}

# Function to setup initial data
setup_initial_data() {
    print_status "Setting up initial data..."
    
    # Run the database setup script
    docker-compose exec -T sre-agent python setup_postgres_db.py
    
    print_success "Initial data setup completed"
}

# Function to display service status
show_status() {
    print_status "Service Status:"
    docker-compose ps
    
    echo ""
    print_status "Service URLs:"
    echo "  SRE Agent API: http://localhost:8000"
    echo "  SRE Dashboard: http://localhost:8501"
    echo "  API Documentation: http://localhost:8000/docs"
    echo "  Grafana: http://localhost:3001 (admin/admin)"
    echo "  Prometheus: http://localhost:9090"
    echo "  Jaeger: http://localhost:16686"
    echo "  LangFuse: http://localhost:3000"
    echo "  Elasticsearch: http://localhost:9200"
    echo "  Nagios: http://localhost:8080 (nagiosadmin/nagios)"
    echo "  Vanguard: http://localhost:8081"
}

# Function to stop services
stop_services() {
    print_status "Stopping services..."
    docker-compose down
    print_success "Services stopped"
}

# Function to clean up
cleanup() {
    print_status "Cleaning up..."
    docker-compose down -v
    docker system prune -f
    print_success "Cleanup completed"
}

# Main deployment function
main() {
    print_status "Starting SRE AI Agent deployment (Final Architecture)..."
    
    check_prerequisites
    create_env_file
    create_ssl_certs
    init_database
    create_monitoring_dirs
    deploy_services
    wait_for_services
    setup_initial_data
    show_status
    
    print_success "SRE AI Agent deployment completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "  1. Access the dashboard at http://localhost:8501"
    echo "  2. View API documentation at http://localhost:8000/docs"
    echo "  3. Monitor services in Grafana at http://localhost:3001"
    echo "  4. Check traces in Jaeger at http://localhost:16686"
    echo ""
    print_status "Default credentials:"
    echo "  - API: admin/admin123, sre_engineer/sre123, viewer/view123"
    echo "  - Grafana: admin/admin"
    echo "  - Nagios: nagiosadmin/nagios"
}

# Parse command line arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "stop")
        stop_services
        ;;
    "cleanup")
        cleanup
        ;;
    "status")
        show_status
        ;;
    "restart")
        stop_services
        main
        ;;
    *)
        echo "Usage: $0 {deploy|stop|cleanup|status|restart}"
        echo "  deploy   - Deploy the complete SRE AI Agent"
        echo "  stop     - Stop all services"
        echo "  cleanup  - Stop and remove all data"
        echo "  status   - Show service status"
        echo "  restart  - Restart all services"
        exit 1
        ;;
esac 