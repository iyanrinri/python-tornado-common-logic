# API Documentation

## Overview

The Tornado Median Calculator Service provides REST API endpoints for calculating the median of two sorted arrays. This document provides detailed information about all available endpoints, request/response formats, and error handling.

## Base Information

- **Base URL**: `http://localhost:8888`
- **Content Type**: `application/json`
- **CORS**: Enabled for all origins
- **Authentication**: None required

## Endpoints

### 1. Calculate Median

Calculate the median of two sorted arrays using an optimized O(log(min(m,n))) algorithm.

**Endpoint**: `POST /api/v1/median`

**Request Body**:
```json
{
  "nums1": [1, 3, 5],
  "nums2": [2, 4, 6]
}
```

**Request Schema**:
- `nums1` (array, required): First sorted array of numbers
- `nums2` (array, required): Second sorted array of numbers

**Validation Rules**:
- Both arrays must contain only numbers (integers or floats)
- Both arrays must be sorted in non-descending order
- Arrays can be empty (but not both)
- No null/undefined values allowed

**Response** (200 OK):
```json
{
  "median": 3.5,
  "array1_size": 3,
  "array2_size": 3,
  "total_elements": 6,
  "execution_time_ms": 0.5
}
```

**Response Schema**:
- `median` (number): The calculated median value
- `array1_size` (integer): Size of the first array
- `array2_size` (integer): Size of the second array  
- `total_elements` (integer): Total number of elements
- `execution_time_ms` (number): Execution time in milliseconds

**Example Usage**:
```bash
curl -X POST http://localhost:8888/api/v1/median \\
  -H "Content-Type: application/json" \\
  -d '{"nums1": [1, 3, 5], "nums2": [2, 4, 6]}'
```

### 2. Batch Median Calculation

Calculate medians for multiple array pairs in a single request.

**Endpoint**: `POST /api/v1/median/batch`

**Request Body**:
```json
{
  "calculations": [
    {"nums1": [1, 3], "nums2": [2, 4]},
    {"nums1": [1, 2], "nums2": [3, 4, 5]},
    {"nums1": [], "nums2": [1, 2, 3]}
  ]
}
```

**Request Schema**:
- `calculations` (array, required): Array of calculation requests
  - Maximum 100 calculations per batch
  - Each calculation follows the same schema as single median calculation

**Response** (200 OK):
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
    },
    {
      "index": 2,
      "median": 2.0,
      "array1_size": 0,
      "array2_size": 3,
      "total_elements": 3,
      "execution_time_ms": 0.1,
      "status": "success"
    }
  ],
  "total_calculations": 3,
  "successful_calculations": 3,
  "failed_calculations": 0
}
```

**Response Schema**:
- `results` (array): Array of calculation results
  - `index` (integer): Index of the calculation in the request
  - `status` (string): "success" or "error"
  - For successful calculations: same fields as single median response
  - For failed calculations: `error_message` and `error_type`
- `total_calculations` (integer): Total number of calculations requested
- `successful_calculations` (integer): Number of successful calculations
- `failed_calculations` (integer): Number of failed calculations

### 3. Service Statistics

Get performance statistics for the median calculation service.

**Endpoint**: `GET /api/v1/median/stats`

**Response** (200 OK):
```json
{
  "total_calls": 42,
  "total_execution_time_ms": 125.5,
  "average_execution_time_ms": 2.99,
  "service_status": "active"
}
```

**Response Schema**:
- `total_calls` (integer): Total number of median calculations performed
- `total_execution_time_ms` (number): Total execution time across all calls
- `average_execution_time_ms` (number): Average execution time per call
- `service_status` (string): Current service status

### 4. Reset Statistics

Reset the service performance statistics.

**Endpoint**: `DELETE /api/v1/median/stats`

**Response** (200 OK):
```json
{
  "message": "Statistics reset successfully"
}
```

## Health Check Endpoints

### 5. Basic Health Check

**Endpoint**: `GET /health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T10:30:00Z",
  "version": "1.0.0",
  "uptime_seconds": 3600.5
}
```

### 6. Detailed Status

**Endpoint**: `GET /status`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T10:30:00Z",
  "version": "1.0.0",
  "uptime_seconds": 3600.5,
  "dependencies": {
    "array_operations_util": "available",
    "logging_system": "active",
    "configuration": "loaded"
  },
  "service_stats": {
    "total_calls": 42,
    "total_execution_time_ms": 125.5,
    "average_execution_time_ms": 2.99,
    "service_status": "active"
  }
}
```

### 7. Readiness Probe

Kubernetes-compatible readiness probe.

**Endpoint**: `GET /ready`

**Response** (200 OK if ready, 503 if not ready):
```json
{
  "status": "ready"
}
```

### 8. Liveness Probe

Kubernetes-compatible liveness probe.

**Endpoint**: `GET /live`

**Response** (200 OK if alive, 503 if not alive):
```json
{
  "status": "alive"
}
```

## Error Handling

All API endpoints return errors in a consistent JSON format:

```json
{
  "error": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "timestamp": "2025-10-23T10:30:00Z",
  "details": {
    "field": "nums1",
    "message": "Array must be sorted"
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `ARRAY_OPERATION_ERROR` | 400 | Array operation error (invalid input) |
| `BATCH_SIZE_ERROR` | 422 | Batch size exceeds maximum limit |
| `BAD_REQUEST` | 400 | Invalid request format or missing data |
| `NOT_FOUND` | 404 | Endpoint not found |
| `METHOD_NOT_ALLOWED` | 405 | HTTP method not supported |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `HEALTH_CHECK_ERROR` | 503 | Health check failed |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

### Validation Errors

For validation errors (422), the `details` field contains specific validation information:

```json
{
  "error": "Request validation failed",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-10-23T10:30:00Z",
  "details": {
    "validation_errors": [
      {
        "field": "nums1",
        "message": "Array must be sorted in non-descending order",
        "type": "value_error",
        "invalid_value": [3, 1, 2]
      }
    ]
  }
}
```

## Request Examples

### Calculate Median with Integers
```bash
curl -X POST http://localhost:8888/api/v1/median \\
  -H "Content-Type: application/json" \\
  -d '{"nums1": [1, 2, 3], "nums2": [4, 5, 6]}'
```

### Calculate Median with Floats
```bash
curl -X POST http://localhost:8888/api/v1/median \\
  -H "Content-Type: application/json" \\
  -d '{"nums1": [1.1, 2.2], "nums2": [1.5, 3.3]}'
```

### Calculate Median with Empty Array
```bash
curl -X POST http://localhost:8888/api/v1/median \\
  -H "Content-Type: application/json" \\
  -d '{"nums1": [], "nums2": [1, 2, 3]}'
```

### Batch Calculation
```bash
curl -X POST http://localhost:8888/api/v1/median/batch \\
  -H "Content-Type: application/json" \\
  -d '{
    "calculations": [
      {"nums1": [1, 3], "nums2": [2, 4]},
      {"nums1": [1, 2], "nums2": [3, 4, 5]}
    ]
  }'
```

### Get Statistics
```bash
curl http://localhost:8888/api/v1/median/stats
```

### Reset Statistics
```bash
curl -X DELETE http://localhost:8888/api/v1/median/stats
```

### Health Checks
```bash
# Basic health
curl http://localhost:8888/health

# Detailed status
curl http://localhost:8888/status

# Readiness probe
curl http://localhost:8888/ready

# Liveness probe  
curl http://localhost:8888/live
```

## CORS Support

The API supports Cross-Origin Resource Sharing (CORS) with the following headers:

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization`

## Rate Limiting

Currently, there is no rate limiting implemented. For production deployments, consider implementing rate limiting at the reverse proxy level or using Tornado middleware.

## Caching

The API does not implement response caching by default. Responses are calculated fresh for each request to ensure accuracy. Consider implementing caching at the application or proxy level if needed for high-traffic scenarios.

## Performance Characteristics

- **Algorithm Complexity**: O(log(min(m,n)))
- **Typical Response Time**: < 1ms for arrays up to 10,000 elements
- **Memory Usage**: O(1) space complexity
- **Batch Processing**: Processes calculations sequentially with individual error handling