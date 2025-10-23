"""
Development and deployment scripts.

This module contains utility scripts for development, testing, and deployment.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_command(command, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    
    return result


def setup_dev_environment():
    """Set up development environment."""
    print("Setting up development environment...")
    
    # Create virtual environment if it doesn't exist
    if not (project_root / "venv").exists():
        run_command("python -m venv venv")
    
    # Install dependencies
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    run_command(f"{pip_cmd} install --upgrade pip")
    run_command(f"{pip_cmd} install -r requirements.txt")
    
    # Create .env file if it doesn't exist
    if not (project_root / ".env").exists():
        run_command("cp .env.example .env")
        print("Created .env file from .env.example")
    
    # Create logs directory
    (project_root / "logs").mkdir(exist_ok=True)
    
    print("Development environment setup complete!")
    print(f"Activate with: source venv/bin/activate (Unix) or venv\\Scripts\\activate (Windows)")


def run_tests():
    """Run the test suite."""
    print("Running test suite...")
    
    # Run tests with coverage
    run_command("pytest --cov=app --cov-report=term-missing --cov-report=html")
    
    print("Tests completed. Coverage report available in htmlcov/index.html")


def run_linting():
    """Run code linting and formatting checks."""
    print("Running code quality checks...")
    
    # Format code with black
    print("Formatting code with black...")
    run_command("black app/ tests/ --check --diff", check=False)
    
    # Lint with flake8
    print("Linting with flake8...")
    run_command("flake8 app/ tests/", check=False)
    
    # Type checking with mypy
    print("Type checking with mypy...")
    run_command("mypy app/", check=False)


def format_code():
    """Format code with black."""
    print("Formatting code...")
    run_command("black app/ tests/")
    print("Code formatting complete!")


def start_server():
    """Start the development server."""
    print("Starting development server...")
    run_command("python main.py --debug=true")


def build_docker():
    """Build Docker image."""
    print("Building Docker image...")
    
    dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \\
    && chown -R app:app /app
USER app

# Create logs directory
RUN mkdir -p logs

EXPOSE 8888

CMD ["python", "main.py", "--port=8888", "--host=0.0.0.0"]
'''
    
    # Write Dockerfile
    with open(project_root / "Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # Build image
    run_command("docker build -t tornado-median-calculator .")
    
    print("Docker image built successfully!")
    print("Run with: docker run -p 8888:8888 tornado-median-calculator")


def deploy_k8s():
    """Generate Kubernetes deployment manifests."""
    print("Generating Kubernetes manifests...")
    
    k8s_manifest = '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: median-calculator
  labels:
    app: median-calculator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: median-calculator
  template:
    metadata:
      labels:
        app: median-calculator
    spec:
      containers:
      - name: median-calculator
        image: tornado-median-calculator:latest
        ports:
        - containerPort: 8888
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "WARNING"
        - name: HOST
          value: "0.0.0.0"
        livenessProbe:
          httpGet:
            path: /live
            port: 8888
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8888
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: median-calculator-service
spec:
  selector:
    app: median-calculator
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8888
  type: LoadBalancer
'''
    
    # Create k8s directory and write manifest
    k8s_dir = project_root / "k8s"
    k8s_dir.mkdir(exist_ok=True)
    
    with open(k8s_dir / "deployment.yaml", "w") as f:
        f.write(k8s_manifest)
    
    print("Kubernetes manifests generated in k8s/deployment.yaml")
    print("Deploy with: kubectl apply -f k8s/deployment.yaml")


def generate_docs():
    """Generate project documentation."""
    print("Generating documentation...")
    
    # Create docs directory
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Generate API documentation (already created)
    print("API documentation available in docs/API.md")
    
    # Generate code documentation with pydoc
    run_command("python -m pydoc -w app.utils.array_operations", check=False)
    run_command("python -m pydoc -w app.services.median_service", check=False)
    
    print("Documentation generation complete!")


def clean_project():
    """Clean project artifacts."""
    print("Cleaning project...")
    
    # Remove cache directories
    cache_dirs = [
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "htmlcov",
        ".coverage",
        "*.egg-info"
    ]
    
    for cache_dir in cache_dirs:
        run_command(f"find . -name '{cache_dir}' -type d -exec rm -rf {{}} + 2>/dev/null || true", check=False)
        run_command(f"find . -name '{cache_dir}' -type f -delete 2>/dev/null || true", check=False)
    
    # Remove log files
    run_command("rm -rf logs/*.log", check=False)
    
    print("Project cleaned!")


def main():
    """Main script entry point."""
    parser = argparse.ArgumentParser(description="Development and deployment scripts")
    parser.add_argument("command", choices=[
        "setup", "test", "lint", "format", "start", "docker", "k8s", "docs", "clean"
    ], help="Command to run")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_dev_environment()
    elif args.command == "test":
        run_tests()
    elif args.command == "lint":
        run_linting()
    elif args.command == "format":
        format_code()
    elif args.command == "start":
        start_server()
    elif args.command == "docker":
        build_docker()
    elif args.command == "k8s":
        deploy_k8s()
    elif args.command == "docs":
        generate_docs()
    elif args.command == "clean":
        clean_project()


if __name__ == "__main__":
    main()