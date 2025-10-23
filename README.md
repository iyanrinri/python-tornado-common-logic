# Tornado Median Calculator Service

A production-ready Tornado-based web service for calculating the median of two sorted arrays, built with clean architecture principles and comprehensive SDLC practices.

## 🎯 Features

- **Efficient Algorithm**: O(log(min(m,n))) median calculation for two sorted arrays
- **REST API**: Clean RESTful endpoints with comprehensive error handling
- **Batch Processing**: Support for multiple median calculations in a single request
- **Production Ready**: Logging, health checks, metrics, and graceful shutdown
- **Clean Architecture**: Separation of concerns with utils, services, and routes layers
- **Comprehensive Testing**: Unit tests, integration tests, and API tests
- **Configuration Management**: Environment-based configuration with validation
- **CORS Support**: Cross-Origin Resource Sharing enabled
- **API Documentation**: Complete OpenAPI/Swagger compatible documentation

## 🏗️ Architecture

```
python-tornado-common-logic/
├── app/                          # Application code
│   ├── utils/                    # Utility functions
│   │   └── array_operations.py   # Core median algorithm
│   ├── services/                 # Business logic layer
│   │   ├── dto.py               # Data Transfer Objects
│   │   └── median_service.py    # Median calculation service
│   └── routes/                  # API endpoints
│       ├── base_handler.py      # Base request handler
│       ├── median_handlers.py   # Median API handlers
│       └── health_handlers.py   # Health check handlers
├── config/                      # Configuration
│   └── settings.py             # Environment settings
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── conftest.py            # Test configuration
├── logs/                       # Log files
├── main.py                     # Application entry point
└── requirements.txt            # Dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-tornado-common-logic
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

The service will start on `http://localhost:8888`

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

## 📚 API Documentation

### Base URL
```
http://localhost:8888
```

### Endpoints

#### Calculate Median
Calculate the median of two sorted arrays.

```http
POST /api/v1/median
Content-Type: application/json

{
  "nums1": [1, 3, 5],
  "nums2": [2, 4, 6]
}
```

**Response:**
```json
{
  "median": 3.5,
  "array1_size": 3,
  "array2_size": 3,
  "total_elements": 6,
  "execution_time_ms": 0.5
}
```

#### Batch Median Calculation
Calculate medians for multiple array pairs.

```http
POST /api/v1/median/batch
Content-Type: application/json

{
  "calculations": [
    {"nums1": [1, 3], "nums2": [2, 4]},
    {"nums1": [1, 2], "nums2": [3, 4, 5]}
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "index": 0,
      "median": 2.5,
      "array1_size": 2,
      "array2_size": 2,
      "total_elements": 4,
      "execution_time_ms": 0.3,
      "status": "success"
    },
    {
      "index": 1,
      "median": 3.0,
      "array1_size": 2,
      "array2_size": 3,
      "total_elements": 5,
      "execution_time_ms": 0.2,
      "status": "success"
    }
  ],
  "total_calculations": 2,
  "successful_calculations": 2,
  "failed_calculations": 0
}
```

#### Service Statistics
Get service performance statistics.

```http
GET /api/v1/median/stats
```

**Response:**
```json
{
  "total_calls": 42,
  "total_execution_time_ms": 125.5,
  "average_execution_time_ms": 2.99,
  "service_status": "active"
}
```

#### Reset Statistics
Reset service statistics.

```http
DELETE /api/v1/median/stats
```

#### Health Checks

- `GET /health` - Basic health check
- `GET /status` - Detailed system status
- `GET /ready` - Readiness probe (K8s compatible)
- `GET /live` - Liveness probe (K8s compatible)

### Error Responses

All errors return JSON in this format:

```json
{
  "error": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "timestamp": "2025-10-23T10:30:00Z",
  "details": {
    "additional": "error details"
  }
}
```

**Error Codes:**
- `VALIDATION_ERROR` (422) - Request validation failed
- `ARRAY_OPERATION_ERROR` (400) - Array operation error
- `BATCH_SIZE_ERROR` (422) - Batch size exceeds limit
- `BAD_REQUEST` (400) - Invalid request format
- `NOT_FOUND` (404) - Endpoint not found
- `METHOD_NOT_ALLOWED` (405) - HTTP method not supported
- `INTERNAL_ERROR` (500) - Internal server error

## 🧮 Algorithm Details

The service implements an optimized **O(log(min(m,n)))** algorithm for finding the median of two sorted arrays without merging them.

### Key Features:
- **Binary Search Approach**: Uses binary search on the smaller array
- **Partition Logic**: Partitions both arrays to find the correct median position
- **Edge Case Handling**: Properly handles empty arrays, single elements, duplicates
- **Type Support**: Works with integers and floating-point numbers
- **Input Validation**: Comprehensive validation of array contents and sorting

### Example Usage:
```python
from app.utils.array_operations import find_median_sorted_arrays

# Basic usage
result = find_median_sorted_arrays([1, 3], [2, 4])  # Returns 2.5

# With empty array
result = find_median_sorted_arrays([], [1, 2, 3])   # Returns 2.0

# With floating point numbers
result = find_median_sorted_arrays([1.1, 2.2], [1.5, 3.3])  # Returns 1.85
```

## 🧪 Testing

The project includes comprehensive testing:

### Test Types:
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and service integration
- **Performance Tests**: Validate algorithm performance characteristics

### Running Tests:

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m api          # API tests only

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# Run performance tests
pytest -m slow

# Generate coverage report
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Test Coverage Goals:
- Minimum 85% code coverage
- 100% coverage for core algorithm
- Comprehensive error case testing

## ⚙️ Configuration

### Environment Variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Environment (development/production/test) |
| `PORT` | `8888` | Server port |
| `HOST` | `localhost` | Server host |
| `DEBUG` | `true` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_FILE` | `logs/app.log` | Log file path |
| `ALLOWED_ORIGINS` | `*` | CORS allowed origins |

### Configuration Files:
- `.env` - Environment variables
- `config/settings.py` - Application configuration
- `pytest.ini` - Test configuration

## 📊 Monitoring and Observability

### Logging
- **Structured Logging**: JSON-formatted logs with correlation IDs
- **Log Rotation**: Automatic log rotation with size limits
- **Log Levels**: Configurable logging levels per environment
- **Request Logging**: All requests logged with timing information

### Health Checks
- **Liveness Probe**: `/live` - Basic functionality test
- **Readiness Probe**: `/ready` - Service ready to accept traffic
- **Health Check**: `/health` - Basic health status
- **Status Check**: `/status` - Detailed system status with dependencies

### Metrics
- **Service Statistics**: Call counts, execution times, error rates
- **Performance Monitoring**: Request/response timing
- **Error Tracking**: Structured error logging and reporting

## 🐳 Deployment

### Docker Support

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8888

CMD ["python", "main.py", "--port=8888"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: median-calculator
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
        image: median-calculator:latest
        ports:
        - containerPort: 8888
        livenessProbe:
          httpGet:
            path: /live
            port: 8888
        readinessProbe:
          httpGet:
            path: /ready
            port: 8888
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "WARNING"
```

## 🔧 Development

### Code Quality Tools:
- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing framework

### Pre-commit Hooks:
```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

### Development Workflow:
1. Create feature branch
2. Implement changes with tests
3. Run quality checks
4. Submit pull request
5. Code review and merge

## 📈 Performance

### Benchmarks:
- **Algorithm Complexity**: O(log(min(m,n)))
- **Memory Usage**: O(1) space complexity
- **Typical Response Time**: < 1ms for arrays up to 10,000 elements
- **Throughput**: > 1000 requests/second (single core)

### Optimization Features:
- **Array Size Optimization**: Always uses smaller array for binary search
- **Input Validation**: Early validation to prevent processing invalid data
- **Response Caching**: Optional response caching for repeated calculations
- **Batch Processing**: Efficient batch processing with parallel execution

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines:
- Write tests for new functionality
- Maintain code coverage above 85%
- Follow PEP 8 style guidelines
- Update documentation for API changes
- Add type hints for all functions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Tornado Web Framework team
- Python community for excellent tooling
- Algorithm inspiration from various computer science resources

---

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the repository
- Contact: your.email@example.com
- Documentation: [Project Wiki](wiki-url)