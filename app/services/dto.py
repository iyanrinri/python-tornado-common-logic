"""
Data Transfer Objects (DTOs) for API communication.

This module defines the data structures used for request/response
handling in the API endpoints.
"""

from typing import List, Union, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
import logging

logger = logging.getLogger(__name__)


class MedianRequest(BaseModel):
    """Request model for median calculation."""
    
    nums1: List[Union[int, float]] = Field(
        ..., 
        description="First sorted array of numbers",
        example=[1, 3, 5]
    )
    nums2: List[Union[int, float]] = Field(
        ..., 
        description="Second sorted array of numbers",
        example=[2, 4, 6]
    )
    
    @validator('nums1', 'nums2')
    def validate_numeric_list(cls, v):
        """Validate that list contains only numeric values."""
        if not isinstance(v, list):
            raise ValueError("Must be a list")
        
        for i, item in enumerate(v):
            if not isinstance(item, (int, float)):
                raise ValueError(f"Item at index {i} must be a number, got {type(item)}")
            if item != item:  # Check for NaN
                raise ValueError(f"Item at index {i} cannot be NaN")
        
        return v
    
    @validator('nums1', 'nums2')
    def validate_sorted(cls, v):
        """Validate that the array is sorted in non-descending order."""
        for i in range(1, len(v)):
            if v[i] < v[i-1]:
                raise ValueError(f"Array must be sorted in non-descending order. "
                               f"Element at index {i} ({v[i]}) is less than "
                               f"element at index {i-1} ({v[i-1]})")
        return v

    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "nums1": [1, 3, 5],
                "nums2": [2, 4, 6]
            }
        }


class MedianResponse(BaseModel):
    """Response model for median calculation."""
    
    median: float = Field(
        ..., 
        description="The calculated median value"
    )
    array1_size: int = Field(
        ..., 
        description="Size of the first array"
    )
    array2_size: int = Field(
        ..., 
        description="Size of the second array"
    )
    total_elements: int = Field(
        ..., 
        description="Total number of elements in both arrays"
    )
    execution_time_ms: Optional[float] = Field(
        None, 
        description="Execution time in milliseconds"
    )
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "median": 3.5,
                "array1_size": 3,
                "array2_size": 3,
                "total_elements": 6,
                "execution_time_ms": 0.5
            }
        }


class ErrorResponse(BaseModel):
    """Response model for error cases."""
    
    error: str = Field(
        ..., 
        description="Error message"
    )
    error_code: str = Field(
        ..., 
        description="Error code for programmatic handling"
    )
    details: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional error details"
    )
    timestamp: Optional[str] = Field(
        None, 
        description="ISO timestamp when error occurred"
    )
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "error": "Array validation failed",
                "error_code": "VALIDATION_ERROR",
                "details": {"field": "nums1", "message": "Array must be sorted"},
                "timestamp": "2025-10-23T10:30:00Z"
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(
        ..., 
        description="Service status"
    )
    timestamp: str = Field(
        ..., 
        description="Current timestamp"
    )
    version: str = Field(
        ..., 
        description="Application version"
    )
    uptime_seconds: float = Field(
        ..., 
        description="Service uptime in seconds"
    )
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-10-23T10:30:00Z",
                "version": "1.0.0",
                "uptime_seconds": 3600.5
            }
        }