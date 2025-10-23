"""
Service layer for median calculation operations.

This module contains the business logic for median calculation,
including validation, processing, and performance monitoring.
"""

import time
import logging
from typing import List, Union, Dict, Any
from datetime import datetime

from ..utils.array_operations import find_median_sorted_arrays, ArrayOperationError
from .dto import MedianRequest, MedianResponse, ErrorResponse

logger = logging.getLogger(__name__)


class MedianCalculationService:
    """Service class for handling median calculation business logic."""
    
    def __init__(self):
        """Initialize the median calculation service."""
        self._call_count = 0
        self._total_execution_time = 0.0
        logger.info("MedianCalculationService initialized")
    
    async def calculate_median(self, request: MedianRequest) -> MedianResponse:
        """
        Calculate the median of two sorted arrays.
        
        Args:
            request: MedianRequest containing the two sorted arrays
            
        Returns:
            MedianResponse: Response containing median and metadata
            
        Raises:
            ArrayOperationError: If calculation fails due to invalid input
        """
        start_time = time.perf_counter()
        
        try:
            logger.info(f"Starting median calculation for arrays of size "
                       f"{len(request.nums1)} and {len(request.nums2)}")
            
            # Perform the median calculation
            median = find_median_sorted_arrays(request.nums1, request.nums2)
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            # Update statistics
            self._call_count += 1
            self._total_execution_time += execution_time_ms
            
            # Create response
            response = MedianResponse(
                median=median,
                array1_size=len(request.nums1),
                array2_size=len(request.nums2),
                total_elements=len(request.nums1) + len(request.nums2),
                execution_time_ms=round(execution_time_ms, 3)
            )
            
            logger.info(f"Median calculation completed successfully. "
                       f"Result: {median}, Execution time: {execution_time_ms:.3f}ms")
            
            return response
            
        except ArrayOperationError as e:
            logger.error(f"Array operation error during median calculation: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during median calculation: {e}")
            raise ArrayOperationError(f"Calculation failed: {str(e)}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get service statistics.
        
        Returns:
            Dict containing service performance statistics
        """
        avg_execution_time = (
            self._total_execution_time / self._call_count 
            if self._call_count > 0 else 0
        )
        
        return {
            "total_calls": self._call_count,
            "total_execution_time_ms": round(self._total_execution_time, 3),
            "average_execution_time_ms": round(avg_execution_time, 3),
            "service_status": "active"
        }
    
    def reset_statistics(self) -> None:
        """Reset service statistics."""
        self._call_count = 0
        self._total_execution_time = 0.0
        logger.info("Service statistics reset")


class HealthService:
    """Service class for health check operations."""
    
    def __init__(self):
        """Initialize the health service."""
        self._start_time = time.time()
        self._version = "1.0.0"
        logger.info("HealthService initialized")
    
    async def get_health_status(self) -> Dict[str, Any]:
        """
        Get the current health status of the service.
        
        Returns:
            Dict containing health information
        """
        current_time = time.time()
        uptime = current_time - self._start_time
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": self._version,
            "uptime_seconds": round(uptime, 1)
        }
    
    def check_dependencies(self) -> Dict[str, str]:
        """
        Check the status of external dependencies.
        
        Returns:
            Dict containing dependency status information
        """
        # In a real application, this would check database connections,
        # external APIs, etc. For this demo, we'll just return basic info.
        return {
            "array_operations_util": "available",
            "logging_system": "active",
            "configuration": "loaded"
        }


# Global service instances
median_service = MedianCalculationService()
health_service = HealthService()