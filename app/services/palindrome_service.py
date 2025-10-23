"""
Service layer for palindrome operations.

This module contains the business logic for palindrome pair calculations,
palindrome checking, and performance monitoring.
"""

import time
import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime

from ..utils.palindrome_operations import (
    find_palindrome_pairs, 
    is_palindrome_optimized, 
    get_palindrome_statistics,
    find_longest_palindrome_pair,
    PalindromeOperationError
)
from .dto_simple import (
    PalindromeRequest, 
    PalindromeResponse, 
    PalindromeCheckRequest, 
    PalindromeCheckResponse
)

logger = logging.getLogger(__name__)


class PalindromeCalculationService:
    """Service class for handling palindrome calculation business logic."""
    
    def __init__(self):
        """Initialize the palindrome calculation service."""
        self._call_count = 0
        self._total_execution_time = 0.0
        self._pairs_found_total = 0
        self._words_processed_total = 0
        logger.info("PalindromeCalculationService initialized")
    
    async def find_palindrome_pairs(self, request: PalindromeRequest) -> PalindromeResponse:
        """
        Find palindrome pairs from a list of words.
        
        Args:
            request: PalindromeRequest containing the list of words
            
        Returns:
            PalindromeResponse: Response containing pairs and metadata
            
        Raises:
            PalindromeOperationError: If calculation fails due to invalid input
        """
        start_time = time.perf_counter()
        
        try:
            logger.info(f"Starting palindrome pairs calculation for {len(request.words)} words")
            
            # Perform the palindrome pairs calculation
            pairs = find_palindrome_pairs(request.words)
            
            # Convert tuples to lists for JSON serialization
            pairs_list = [list(pair) for pair in pairs]
            
            # Get additional statistics
            stats = get_palindrome_statistics(request.words)
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            # Update service statistics
            self._call_count += 1
            self._total_execution_time += execution_time_ms
            self._pairs_found_total += len(pairs)
            self._words_processed_total += len(request.words)
            
            # Create response
            response = PalindromeResponse(
                pairs=pairs_list,
                word_count=len(request.words),
                pairs_count=len(pairs),
                execution_time_ms=round(execution_time_ms, 3),
                statistics=stats
            )
            
            logger.info(f"Palindrome pairs calculation completed successfully. "
                       f"Found {len(pairs)} pairs, Execution time: {execution_time_ms:.3f}ms")
            
            return response
            
        except PalindromeOperationError as e:
            logger.error(f"Palindrome operation error during calculation: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during palindrome calculation: {e}")
            raise PalindromeOperationError(f"Calculation failed: {str(e)}")
    
    async def check_palindrome(self, request: PalindromeCheckRequest) -> PalindromeCheckResponse:
        """
        Check if a single text is a palindrome.
        
        Args:
            request: PalindromeCheckRequest containing the text to check
            
        Returns:
            PalindromeCheckResponse: Response containing the result
            
        Raises:
            PalindromeOperationError: If check fails due to invalid input
        """
        start_time = time.perf_counter()
        
        try:
            logger.debug(f"Checking if text is palindrome: '{request.text}'")
            
            # Check if text is palindrome
            is_palindrome_result = is_palindrome_optimized(request.text)
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            # Create response
            response = PalindromeCheckResponse(
                text=request.text,
                is_palindrome=is_palindrome_result,
                execution_time_ms=round(execution_time_ms, 3)
            )
            
            logger.debug(f"Palindrome check completed: {is_palindrome_result}, "
                        f"Execution time: {execution_time_ms:.3f}ms")
            
            return response
            
        except PalindromeOperationError as e:
            logger.error(f"Palindrome operation error during check: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during palindrome check: {e}")
            raise PalindromeOperationError(f"Palindrome check failed: {str(e)}")
    
    async def find_longest_palindrome_pair(self, request: PalindromeRequest) -> Dict[str, Any]:
        """
        Find the longest palindrome pair from a list of words.
        
        Args:
            request: PalindromeRequest containing the list of words
            
        Returns:
            Dict containing the longest palindrome pair information
        """
        start_time = time.perf_counter()
        
        try:
            logger.info(f"Finding longest palindrome pair from {len(request.words)} words")
            
            # Find the longest palindrome pair
            longest_pair_result = find_longest_palindrome_pair(request.words)
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            if longest_pair_result is None:
                result = {
                    "found": False,
                    "message": "No palindrome pairs found",
                    "execution_time_ms": round(execution_time_ms, 3)
                }
            else:
                index1, index2, length = longest_pair_result
                palindrome_text = request.words[index1] + request.words[index2]
                result = {
                    "found": True,
                    "indices": [index1, index2],
                    "words": [request.words[index1], request.words[index2]],
                    "palindrome": palindrome_text,
                    "length": length,
                    "execution_time_ms": round(execution_time_ms, 3)
                }
            
            logger.info(f"Longest palindrome pair search completed. "
                       f"Found: {result['found']}, Execution time: {execution_time_ms:.3f}ms")
            
            return result
            
        except PalindromeOperationError as e:
            logger.error(f"Palindrome operation error during longest pair search: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during longest pair search: {e}")
            raise PalindromeOperationError(f"Longest pair search failed: {str(e)}")
    
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
        
        avg_pairs_per_call = (
            self._pairs_found_total / self._call_count
            if self._call_count > 0 else 0
        )
        
        avg_words_per_call = (
            self._words_processed_total / self._call_count
            if self._call_count > 0 else 0
        )
        
        return {
            "total_calls": self._call_count,
            "total_execution_time_ms": round(self._total_execution_time, 3),
            "average_execution_time_ms": round(avg_execution_time, 3),
            "total_pairs_found": self._pairs_found_total,
            "total_words_processed": self._words_processed_total,
            "average_pairs_per_call": round(avg_pairs_per_call, 2),
            "average_words_per_call": round(avg_words_per_call, 2),
            "service_status": "active"
        }
    
    def reset_statistics(self) -> None:
        """Reset service statistics."""
        self._call_count = 0
        self._total_execution_time = 0.0
        self._pairs_found_total = 0
        self._words_processed_total = 0
        logger.info("Palindrome service statistics reset")


# Global service instance
palindrome_service = PalindromeCalculationService()