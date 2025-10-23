"""
API handlers for median calculation endpoints - Simple version without Pydantic.

This module contains Tornado request handlers for the median calculation API,
including validation, error handling, and response formatting.
"""

import logging
from typing import Dict, Any

from tornado.web import HTTPError

from .base_handler import BaseHandler
from ..services import median_service
from ..services.dto_simple import MedianRequest, MedianResponse, ValidationError
from ..utils.array_operations import ArrayOperationError

logger = logging.getLogger(__name__)


class MedianHandler(BaseHandler):
    """Handler for median calculation operations."""
    
    async def post(self):
        """
        Calculate the median of two sorted arrays.
        
        Request body:
        {
            "nums1": [1, 3, 5],
            "nums2": [2, 4, 6]
        }
        
        Response:
        {
            "median": 3.5,
            "array1_size": 3,
            "array2_size": 3,
            "total_elements": 6,
            "execution_time_ms": 0.5
        }
        """
        try:
            # Parse and validate request body
            body = self.get_json_body()
            
            # Validate request using simple validation
            try:
                request = MedianRequest.from_dict(body)
            except ValidationError as e:
                logger.warning(f"Request validation failed: {e}")
                error_details = {
                    "validation_errors": [{
                        "field": e.field or "unknown",
                        "message": e.message,
                        "type": "validation_error"
                    }]
                }
                self.write_error_json(
                    error_message="Request validation failed",
                    error_code="VALIDATION_ERROR",
                    status_code=422,
                    details=error_details
                )
                return
            
            # Calculate median using service
            try:
                response = await median_service.calculate_median(request)
                
                # Convert to dictionary for JSON response
                response_dict = response.to_dict()
                
                self.write_json(response_dict, 200)
                
            except ArrayOperationError as e:
                logger.error(f"Array operation error: {e}")
                self.write_error_json(
                    error_message=str(e),
                    error_code="ARRAY_OPERATION_ERROR",
                    status_code=400
                )
                return
            
        except HTTPError:
            # Re-raise HTTP errors (already handled by base class)
            raise
        except Exception as e:
            logger.error(f"Unexpected error in MedianHandler: {e}", exc_info=True)
            self.write_error_json(
                error_message="Internal server error",
                error_code="INTERNAL_ERROR",
                status_code=500
            )


class MedianStatsHandler(BaseHandler):
    """Handler for median service statistics."""
    
    async def get(self):
        """
        Get median calculation service statistics.
        
        Response:
        {
            "total_calls": 42,
            "total_execution_time_ms": 125.5,
            "average_execution_time_ms": 2.99,
            "service_status": "active"
        }
        """
        try:
            stats = median_service.get_statistics()
            self.write_json(stats, 200)
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}", exc_info=True)
            self.write_error_json(
                error_message="Failed to retrieve statistics",
                error_code="STATS_ERROR",
                status_code=500
            )
    
    async def delete(self):
        """
        Reset median calculation service statistics.
        
        Response:
        {
            "message": "Statistics reset successfully"
        }
        """
        try:
            median_service.reset_statistics()
            self.write_json({"message": "Statistics reset successfully"}, 200)
            
        except Exception as e:
            logger.error(f"Error resetting statistics: {e}", exc_info=True)
            self.write_error_json(
                error_message="Failed to reset statistics", 
                error_code="STATS_RESET_ERROR",
                status_code=500
            )


class MedianBatchHandler(BaseHandler):
    """Handler for batch median calculations."""
    
    async def post(self):
        """
        Calculate medians for multiple array pairs.
        
        Request body:
        {
            "calculations": [
                {"nums1": [1, 3], "nums2": [2, 4]},
                {"nums1": [1, 2], "nums2": [3, 4, 5]}
            ]
        }
        
        Response:
        {
            "results": [
                {"median": 2.5, "array1_size": 2, "array2_size": 2, ...},
                {"median": 3.0, "array1_size": 2, "array2_size": 3, ...}
            ],
            "total_calculations": 2,
            "successful_calculations": 2,
            "failed_calculations": 0
        }
        """
        try:
            body = self.get_json_body()
            
            if "calculations" not in body or not isinstance(body["calculations"], list):
                self.write_error_json(
                    error_message="Request must contain 'calculations' array",
                    error_code="VALIDATION_ERROR",
                    status_code=422
                )
                return
            
            calculations = body["calculations"]
            
            if len(calculations) > 100:  # Limit batch size
                self.write_error_json(
                    error_message="Batch size cannot exceed 100 calculations",
                    error_code="BATCH_SIZE_ERROR",
                    status_code=422
                )
                return
            
            results = []
            successful = 0
            failed = 0
            
            for i, calc in enumerate(calculations):
                try:
                    # Validate individual calculation request
                    request = MedianRequest.from_dict(calc)
                    response = await median_service.calculate_median(request)
                    
                    result = {
                        "index": i,
                        **response.to_dict(),
                        "status": "success"
                    }
                    
                    successful += 1
                    
                except (ValidationError, ArrayOperationError) as e:
                    result = {
                        "index": i,
                        "status": "error",
                        "error_message": str(e),
                        "error_type": type(e).__name__
                    }
                    failed += 1
                
                results.append(result)
            
            response_data = {
                "results": results,
                "total_calculations": len(calculations),
                "successful_calculations": successful,
                "failed_calculations": failed
            }
            
            self.write_json(response_data, 200)
            
        except HTTPError:
            raise
        except Exception as e:
            logger.error(f"Error in batch calculation: {e}", exc_info=True)
            self.write_error_json(
                error_message="Batch calculation failed",
                error_code="BATCH_ERROR",
                status_code=500
            )