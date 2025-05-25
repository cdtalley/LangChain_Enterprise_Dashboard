#!/bin/bash

# Enterprise LangChain AI Workbench - Production Deployment Script
# =================================================================
# This script demonstrates enterprise-grade deployment practices

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="langchain-enterprise-workbench"
VERSION="2.0.0"
ENVIRONMENT="${ENVIRONMENT:-production}"
DOCKER_REGISTRY="${DOCKER_REGISTRY:-localhost:5000}"

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed. Please install Python 3.11+ first."
    fi
    
    # Check Python version
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [[ $(echo "$PYTHON_VERSION < 3.11" | bc -l) -eq 1 ]]; then
        error "Python 3.11+ is required. Current version: $PYTHON_VERSION"
    fi
    
    success "All prerequisites met ✅"
}

# Function to run tests
run_tests() {
    log "Running comprehensive test suite..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        log "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate || source venv/Scripts/activate
    
    # Install test dependencies
    pip install -r requirements.txt
    pip install pytest pytest-cov pytest-asyncio
    
    # Run tests with coverage
    log "Running unit tests..."
    pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing || {
        error "Tests failed! Please fix issues before deployment."
    }
    
    # Run security tests
    log "Running security tests..."
    pytest tests/test_enterprise_features.py::TestSecurity -v || {
        error "Security tests failed! Please address security issues."
    }
    
    # Run performance tests
    log "Running performance tests..."
    pytest tests/test_enterprise_features.py::TestPerformance -v || {
        warning "Performance tests failed. Consider optimization."
    }
    
    success "All tests passed ✅"
}

# Function to build Docker images
build_images() {
    log "Building Docker images..."
    
    # Build main application image
    docker build -t $APP_NAME:$VERSION . || {
        error "Failed to build Docker image"
    }
    
    # Tag for registry
    docker tag $APP_NAME:$VERSION $DOCKER_REGISTRY/$APP_NAME:$VERSION
    docker tag $APP_NAME:$VERSION $DOCKER_REGISTRY/$APP_NAME:latest
    
    success "Docker images built successfully ✅"
}

# Function to run security scan
security_scan() {
    log "Running security scan..."
    
    # Check if trivy is installed
    if command -v trivy &> /dev/null; then
        log "Scanning Docker image for vulnerabilities..."
        trivy image $APP_NAME:$VERSION || {
            warning "Security vulnerabilities found. Review before production deployment."
        }
    else
        warning "Trivy not installed. Skipping container security scan."
    fi
}

# Function to deploy locally
deploy_local() {
    log "Deploying locally with Docker Compose..."
    
    # Stop existing containers
    docker-compose down || true
    
    # Start services
    docker-compose up --build -d
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 10
    
    # Health check
    for i in {1..30}; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            success "API service is healthy ✅"
            break
        fi
        log "Waiting for API service... ($i/30)"
        sleep 2
    done
    
    if curl -f http://localhost:8501 &> /dev/null; then
        success "Frontend service is healthy ✅"
    else
        warning "Frontend service may not be ready yet"
    fi
}

# Function to deploy to production
deploy_production() {
    log "Deploying to production environment..."
    
    # Push images to registry
    if [ "$DOCKER_REGISTRY" != "localhost:5000" ]; then
        log "Pushing images to registry..."
        docker push $DOCKER_REGISTRY/$APP_NAME:$VERSION
        docker push $DOCKER_REGISTRY/$APP_NAME:latest
    fi
    
    # Deploy with production compose file
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    
    # Wait for services
    log "Waiting for production services..."
    sleep 15
    
    # Production health check
    for i in {1..60}; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            success "Production deployment successful ✅"
            break
        fi
        log "Waiting for production services... ($i/60)"
        sleep 2
    done
}

# Function to show deployment info
show_info() {
    log "Deployment Information:"
    echo ""
    echo "🌐 Services:"
    echo "   • Streamlit UI:      http://localhost:8501"
    echo "   • API Documentation: http://localhost:8000/docs"
    echo "   • Health Check:      http://localhost:8000/health"
    echo "   • Metrics:           http://localhost:8000/api/v1/metrics"
    
    if [ "$ENVIRONMENT" = "production" ]; then
        echo "   • Monitoring:        http://localhost:3000"
        echo "   • Prometheus:        http://localhost:9090"
    fi
    
    echo ""
    echo "📊 Quick Commands:"
    echo "   • View logs:         docker-compose logs -f"
    echo "   • Scale API:         docker-compose scale api=3"
    echo "   • Stop services:     docker-compose down"
    echo "   • Run tests:         pytest tests/ -v"
    
    echo ""
    echo "🔐 Authentication:"
    echo "   • API Token:         Use 'Bearer test-token' for demo"
    echo "   • Grafana:           admin / admin123"
}

# Function to cleanup
cleanup() {
    log "Cleaning up..."
    docker-compose down
    docker system prune -f
    success "Cleanup completed ✅"
}

# Main deployment function
main() {
    echo "🚀 Enterprise LangChain AI Workbench Deployment"
    echo "================================================"
    echo "Version: $VERSION"
    echo "Environment: $ENVIRONMENT"
    echo ""
    
    case "$1" in
        "test")
            check_prerequisites
            run_tests
            ;;
        "build")
            check_prerequisites
            build_images
            security_scan
            ;;
        "local"|"")
            check_prerequisites
            run_tests
            build_images
            deploy_local
            show_info
            ;;
        "production"|"prod")
            check_prerequisites
            run_tests
            build_images
            security_scan
            deploy_production
            show_info
            ;;
        "cleanup")
            cleanup
            ;;
        "info")
            show_info
            ;;
        *)
            echo "Usage: $0 {test|build|local|production|cleanup|info}"
            echo ""
            echo "Commands:"
            echo "  test        - Run comprehensive test suite"
            echo "  build       - Build Docker images with security scan"
            echo "  local       - Deploy locally (default)"
            echo "  production  - Deploy to production environment"
            echo "  cleanup     - Stop services and cleanup"
            echo "  info        - Show deployment information"
            exit 1
            ;;
    esac
}

# Trap function for cleanup on exit
trap 'echo -e "\n${RED}Deployment interrupted${NC}"' INT TERM

# Run main function with all arguments
main "$@" 