"""
Simple Data Transfer Objects (DTOs) for API communication - No Pydantic dependency.

This module defines the data structures used for request/response
handling in the API endpoints using basic Python classes with validation.
"""

from typing import List, Union, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(message)


class MedianRequest:
    """Request model for median calculation."""
    
    def __init__(self, nums1: List[Union[int, float]], nums2: List[Union[int, float]]):
        """Initialize and validate the request."""
        self.nums1 = self._validate_numeric_list(nums1, "nums1")
        self.nums2 = self._validate_numeric_list(nums2, "nums2")
        self._validate_sorted(self.nums1, "nums1")
        self._validate_sorted(self.nums2, "nums2")
    
    def _validate_numeric_list(self, value: Any, field_name: str) -> List[Union[int, float]]:
        """Validate that list contains only numeric values."""
        if not isinstance(value, list):
            raise ValidationError(f"Field '{field_name}' must be a list", field_name)
        
        for i, item in enumerate(value):
            if not isinstance(item, (int, float)):
                raise ValidationError(
                    f"Item at index {i} in '{field_name}' must be a number, got {type(item).__name__}",
                    field_name
                )
            if item != item:  # Check for NaN
                raise ValidationError(f"Item at index {i} in '{field_name}' cannot be NaN", field_name)
        
        return value
    
    def _validate_sorted(self, value: List[Union[int, float]], field_name: str) -> None:
        """Validate that the array is sorted in non-descending order."""
        for i in range(1, len(value)):
            if value[i] < value[i-1]:
                raise ValidationError(
                    f"Array '{field_name}' must be sorted in non-descending order. "
                    f"Element at index {i} ({value[i]}) is less than "
                    f"element at index {i-1} ({value[i-1]})",
                    field_name
                )
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MedianRequest':
        """Create MedianRequest from dictionary."""
        if not isinstance(data, dict):
            raise ValidationError("Request data must be a dictionary")
        
        if "nums1" not in data:
            raise ValidationError("Missing required field 'nums1'", "nums1")
        if "nums2" not in data:
            raise ValidationError("Missing required field 'nums2'", "nums2")
        
        return cls(nums1=data["nums1"], nums2=data["nums2"])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "nums1": self.nums1,
            "nums2": self.nums2
        }


class MedianResponse:
    """Response model for median calculation."""
    
    def __init__(self, median: float, array1_size: int, array2_size: int, 
                 total_elements: int, execution_time_ms: Optional[float] = None):
        """Initialize the response."""
        self.median = median
        self.array1_size = array1_size
        self.array2_size = array2_size
        self.total_elements = total_elements
        self.execution_time_ms = execution_time_ms
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response."""
        result = {
            "median": self.median,
            "array1_size": self.array1_size,
            "array2_size": self.array2_size,
            "total_elements": self.total_elements
        }
        
        if self.execution_time_ms is not None:
            result["execution_time_ms"] = self.execution_time_ms
        
        return result


class ErrorResponse:
    """Response model for error cases."""
    
    def __init__(self, error: str, error_code: str, details: Optional[Dict[str, Any]] = None, 
                 timestamp: Optional[str] = None):
        """Initialize the error response."""
        self.error = error
        self.error_code = error_code
        self.details = details
        self.timestamp = timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response."""
        result = {
            "error": self.error,
            "error_code": self.error_code
        }
        
        if self.timestamp:
            result["timestamp"] = self.timestamp
        
        if self.details:
            result["details"] = self.details
        
        return result


class HealthResponse:
    """Response model for health check."""
    
    def __init__(self, status: str, timestamp: str, version: str, uptime_seconds: float):
        """Initialize the health response."""
        self.status = status
        self.timestamp = timestamp
        self.version = version
        self.uptime_seconds = uptime_seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response."""
        return {
            "status": self.status,
            "timestamp": self.timestamp,
            "version": self.version,
            "uptime_seconds": self.uptime_seconds
        }