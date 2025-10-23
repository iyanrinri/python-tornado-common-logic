"""
API handlers for palindrome operations endpoints.

This module contains Tornado request handlers for palindrome pairs and
palindrome checking API endpoints, including validation, error handling,
and response formatting.
"""

import logging
from typing import Dict, Any

from tornado.web import HTTPError

from .base_handler import BaseHandler
from ..services.palindrome_service import palindrome_service
from ..services.dto_simple import (
    PalindromeRequest, 
    PalindromeCheckRequest, 
    ValidationError
)
from ..utils.palindrome_operations import PalindromeOperationError

logger = logging.getLogger(__name__)


class PalindromeHandler(BaseHandler):
    """Handler for palindrome pairs calculation operations."""
    
    async def post(self):
        """
        Find palindrome pairs from a list of words.
        
        Request body:
        {
            "words": ["lls", "s", "sssll"]
        }
        
        Response:
        {
            "pairs": [[0, 1], [1, 0], [2, 0]],
            "word_count": 3,
            "pairs_count": 3,
            "execution_time_ms": 0.5,
            "statistics": {
                "total_words": 3,
                "palindrome_pairs_count": 3,
                "unique_words_in_pairs": 3,
                "examples": [...],
                "has_palindromes": true
            }
        }
        """
        try:
            # Parse and validate request body
            body = self.get_json_body()
            
            # Validate request using simple validation
            try:
                request = PalindromeRequest.from_dict(body)
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
            
            # Calculate palindrome pairs using service
            try:
                response = await palindrome_service.find_palindrome_pairs(request)
                
                # Convert to dictionary for JSON response
                response_dict = response.to_dict()
                
                self.write_json(response_dict, 200)
                
            except PalindromeOperationError as e:
                logger.error(f"Palindrome operation error: {e}")
                self.write_error_json(
                    error_message=str(e),
                    error_code="PALINDROME_OPERATION_ERROR",
                    status_code=400
                )
                return
            
        except HTTPError:
            # Re-raise HTTP errors (already handled by base class)
            raise
        except Exception as e:
            logger.error(f"Unexpected error in PalindromeHandler: {e}", exc_info=True)
            self.write_error_json(
                error_message="Internal server error",
                error_code="INTERNAL_ERROR",
                status_code=500
            )


class PalindromeCheckHandler(BaseHandler):
    """Handler for single palindrome check operations."""
    
    async def post(self):
        """
        Check if a text is a palindrome.
        
        Request body:
        {
            "text": "racecar"
        }
        
        Response:
        {
            "text": "racecar",
            "is_palindrome": true,
            "execution_time_ms": 0.1
        }
        """
        try:
            # Parse and validate request body
            body = self.get_json_body()
            
            # Validate request
            try:
                request = PalindromeCheckRequest.from_dict(body)
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
            
            # Check palindrome using service
            try:
                response = await palindrome_service.check_palindrome(request)
                
                # Convert to dictionary for JSON response
                response_dict = response.to_dict()
                
                self.write_json(response_dict, 200)
                
            except PalindromeOperationError as e:
                logger.error(f"Palindrome operation error: {e}")
                self.write_error_json(
                    error_message=str(e),
                    error_code="PALINDROME_OPERATION_ERROR",
                    status_code=400
                )
                return
            
        except HTTPError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in PalindromeCheckHandler: {e}", exc_info=True)
            self.write_error_json(
                error_message="Internal server error",
                error_code="INTERNAL_ERROR",
                status_code=500
            )


class PalindromeLongestHandler(BaseHandler):
    """Handler for finding the longest palindrome pair."""
    
    async def post(self):
        """
        Find the longest palindrome pair from a list of words.
        
        Request body:
        {
            "words": ["abc", "cba", "def", "fed"]
        }
        
        Response:
        {
            "found": true,
            "indices": [0, 1],
            "words": ["abc", "cba"],
            "palindrome": "abccba",
            "length": 6,
            "execution_time_ms": 0.3
        }
        """
        try:
            # Parse and validate request body
            body = self.get_json_body()
            
            # Validate request
            try:
                request = PalindromeRequest.from_dict(body)
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
            
            # Find longest palindrome pair using service
            try:
                response_dict = await palindrome_service.find_longest_palindrome_pair(request)
                
                self.write_json(response_dict, 200)
                
            except PalindromeOperationError as e:
                logger.error(f"Palindrome operation error: {e}")
                self.write_error_json(
                    error_message=str(e),
                    error_code="PALINDROME_OPERATION_ERROR",
                    status_code=400
                )
                return
            
        except HTTPError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in PalindromeLongestHandler: {e}", exc_info=True)
            self.write_error_json(
                error_message="Internal server error",
                error_code="INTERNAL_ERROR",
                status_code=500
            )


class PalindromeStatsHandler(BaseHandler):
    """Handler for palindrome service statistics."""
    
    async def get(self):
        """
        Get palindrome calculation service statistics.
        
        Response:
        {
            "total_calls": 15,
            "total_execution_time_ms": 45.2,
            "average_execution_time_ms": 3.01,
            "total_pairs_found": 28,
            "total_words_processed": 150,
            "average_pairs_per_call": 1.87,
            "average_words_per_call": 10.0,
            "service_status": "active"
        }
        """
        try:
            stats = palindrome_service.get_statistics()
            self.write_json(stats, 200)
            
        except Exception as e:
            logger.error(f"Error getting palindrome statistics: {e}", exc_info=True)
            self.write_error_json(
                error_message="Failed to retrieve statistics",
                error_code="STATS_ERROR",
                status_code=500
            )
    
    async def delete(self):
        """
        Reset palindrome calculation service statistics.
        
        Response:
        {
            "message": "Palindrome service statistics reset successfully"
        }
        """
        try:
            palindrome_service.reset_statistics()
            self.write_json({"message": "Palindrome service statistics reset successfully"}, 200)
            
        except Exception as e:
            logger.error(f"Error resetting palindrome statistics: {e}", exc_info=True)
            self.write_error_json(
                error_message="Failed to reset palindrome statistics",
                error_code="STATS_RESET_ERROR",
                status_code=500
            )


class PalindromeBatchHandler(BaseHandler):
    """Handler for batch palindrome operations."""
    
    async def post(self):
        """
        Process multiple palindrome operations in batch.
        
        Request body:
        {
            "operations": [
                {"type": "pairs", "words": ["abc", "cba"]},
                {"type": "check", "text": "racecar"},
                {"type": "longest", "words": ["ab", "ba", "xyz"]}
            ]
        }
        
        Response:
        {
            "results": [
                {"index": 0, "type": "pairs", "status": "success", "result": {...}},
                {"index": 1, "type": "check", "status": "success", "result": {...}},
                {"index": 2, "type": "longest", "status": "success", "result": {...}}
            ],
            "total_operations": 3,
            "successful_operations": 3,
            "failed_operations": 0
        }
        """
        try:
            body = self.get_json_body()
            
            if "operations" not in body or not isinstance(body["operations"], list):
                self.write_error_json(
                    error_message="Request must contain 'operations' array",
                    error_code="VALIDATION_ERROR",
                    status_code=422
                )
                return
            
            operations = body["operations"]
            
            if len(operations) > 50:  # Limit batch size
                self.write_error_json(
                    error_message="Batch size cannot exceed 50 operations",
                    error_code="BATCH_SIZE_ERROR",
                    status_code=422
                )
                return
            
            results = []
            successful = 0
            failed = 0
            
            for i, operation in enumerate(operations):
                try:
                    op_type = operation.get("type")
                    result = {"index": i, "type": op_type}
                    
                    if op_type == "pairs":
                        request = PalindromeRequest.from_dict({"words": operation.get("words", [])})
                        response = await palindrome_service.find_palindrome_pairs(request)
                        result.update({"status": "success", "result": response.to_dict()})
                        
                    elif op_type == "check":
                        request = PalindromeCheckRequest.from_dict({"text": operation.get("text", "")})
                        response = await palindrome_service.check_palindrome(request)
                        result.update({"status": "success", "result": response.to_dict()})
                        
                    elif op_type == "longest":
                        request = PalindromeRequest.from_dict({"words": operation.get("words", [])})
                        response = await palindrome_service.find_longest_palindrome_pair(request)
                        result.update({"status": "success", "result": response})
                        
                    else:
                        result.update({
                            "status": "error",
                            "error_message": f"Unknown operation type: {op_type}",
                            "error_type": "ValidationError"
                        })
                        failed += 1
                        results.append(result)
                        continue
                    
                    successful += 1
                    
                except (ValidationError, PalindromeOperationError) as e:
                    result.update({
                        "status": "error",
                        "error_message": str(e),
                        "error_type": type(e).__name__
                    })
                    failed += 1
                
                results.append(result)
            
            response_data = {
                "results": results,
                "total_operations": len(operations),
                "successful_operations": successful,
                "failed_operations": failed
            }
            
            self.write_json(response_data, 200)
            
        except HTTPError:
            raise
        except Exception as e:
            logger.error(f"Error in palindrome batch operation: {e}", exc_info=True)
            self.write_error_json(
                error_message="Palindrome batch operation failed",
                error_code="BATCH_ERROR",
                status_code=500
            )