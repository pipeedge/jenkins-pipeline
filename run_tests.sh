#!/bin/bash

# Calculator Application - Local Test Runner
# This script runs the same checks as the Jenkins pipeline locally

set -e  # Exit on any error

echo "=================================================="
echo "Calculator Application - Local Test Runner"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip and install dependencies
print_status "Installing/updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=================================================="
echo "Running Code Quality Checks"
echo "=================================================="

# Flake8 linting
print_status "Running Flake8 linting..."
if flake8 --max-line-length=100 --exclude=venv --statistics .; then
    print_success "Flake8 linting passed"
else
    print_error "Flake8 linting failed"
    exit 1
fi

echo ""

# Black code formatting check
print_status "Checking code formatting with Black..."
if black --check --line-length=100 --exclude=venv .; then
    print_success "Code formatting check passed"
else
    print_warning "Code needs formatting. Run 'black --line-length=100 .' to fix"
    # Don't exit on formatting issues, just warn
fi

echo ""

# MyPy type checking
print_status "Running MyPy type checking..."
if mypy --ignore-missing-imports --no-strict-optional calculator.py; then
    print_success "Type checking passed"
else
    print_error "Type checking failed"
    exit 1
fi

echo ""
echo "=================================================="
echo "Running Security Scan"
echo "=================================================="

# Bandit security scan
print_status "Running Bandit security scan..."
if bandit -r . --exclude ./venv; then
    print_success "Security scan passed - no issues found"
else
    print_warning "Security scan found potential issues - please review"
    # Don't exit on security warnings in development
fi

echo ""
echo "=================================================="
echo "Running Unit Tests"
echo "=================================================="

# Run pytest with coverage
print_status "Running unit tests with coverage..."
if pytest -v --cov=calculator --cov-report=html --cov-report=term-missing --cov-report=xml; then
    print_success "All tests passed!"
else
    print_error "Some tests failed"
    exit 1
fi

echo ""
echo "=================================================="
echo "Running Integration Tests"
echo "=================================================="

# Run calculator demo
print_status "Running calculator demo..."
if python calculator.py; then
    print_success "Calculator demo completed successfully"
else
    print_error "Calculator demo failed"
    exit 1
fi

echo ""
echo "=================================================="
echo "Test Summary"
echo "=================================================="

print_success "All checks completed successfully!"
echo ""
echo "📊 Reports generated:"
echo "   - HTML Coverage Report: htmlcov/index.html"
echo "   - XML Coverage Report: coverage.xml"
echo ""
echo "🚀 Ready for Jenkins pipeline execution!"

# Display coverage summary
if [ -f ".coverage" ]; then
    echo ""
    print_status "Coverage Summary:"
    coverage report --show-missing
fi

echo ""
echo "==================================================" 