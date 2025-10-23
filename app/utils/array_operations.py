"""
Utility functions for array operations.

This module contains optimized algorithms for common array operations,
including finding the median of two sorted arrays.
"""

from typing import List, Union, Optional
import logging

logger = logging.getLogger(__name__)


class ArrayOperationError(Exception):
    """Custom exception for array operation errors."""
    pass


def find_median_sorted_arrays(nums1: List[Union[int, float]], 
                             nums2: List[Union[int, float]]) -> float:
    """
    Find the median of two sorted arrays.
    
    This function implements an optimized O(log(min(m,n))) algorithm
    to find the median of two sorted arrays without merging them.
    
    Args:
        nums1: First sorted array of integers or floats
        nums2: Second sorted array of integers or floats
        
    Returns:
        float: The median value of the combined arrays
        
    Raises:
        ArrayOperationError: If arrays are None, contain invalid values,
                           or are not properly sorted
        
    Examples:
        >>> find_median_sorted_arrays([1, 3], [2])
        2.0
        >>> find_median_sorted_arrays([1, 2], [3, 4])
        2.5
        >>> find_median_sorted_arrays([], [1])
        1.0
    """
    # Input validation
    if nums1 is None or nums2 is None:
        raise ArrayOperationError("Input arrays cannot be None")
    
    # Validate array contents
    _validate_array_contents(nums1, "nums1")
    _validate_array_contents(nums2, "nums2")
    
    # Validate arrays are sorted
    _validate_array_sorted(nums1, "nums1")
    _validate_array_sorted(nums2, "nums2")
    
    logger.debug(f"Finding median for arrays of size {len(nums1)} and {len(nums2)}")
    
    # Handle edge cases
    if len(nums1) == 0 and len(nums2) == 0:
        raise ArrayOperationError("Both arrays cannot be empty")
    
    if len(nums1) == 0:
        return _find_median_single_array(nums2)
    
    if len(nums2) == 0:
        return _find_median_single_array(nums1)
    
    # Ensure nums1 is the smaller array for optimization
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    total = m + n
    half = (total + 1) // 2
    
    left, right = 0, m
    
    while left <= right:
        partition_x = (left + right) // 2
        partition_y = half - partition_x
        
        # Handle edge cases for partition boundaries
        max_left_x = float('-inf') if partition_x == 0 else nums1[partition_x - 1]
        min_right_x = float('inf') if partition_x == m else nums1[partition_x]
        
        max_left_y = float('-inf') if partition_y == 0 else nums2[partition_y - 1]
        min_right_y = float('inf') if partition_y == n else nums2[partition_y]
        
        # Check if we found the correct partition
        if max_left_x <= min_right_y and max_left_y <= min_right_x:
            # Found the correct partition
            if total % 2 == 1:
                # Odd total length - return the middle element
                median = max(max_left_x, max_left_y)
            else:
                # Even total length - return average of two middle elements
                left_max = max(max_left_x, max_left_y)
                right_min = min(min_right_x, min_right_y)
                median = (left_max + right_min) / 2.0
            
            logger.debug(f"Calculated median: {median}")
            return float(median)
        
        elif max_left_x > min_right_y:
            # We have partitioned too far to the right in nums1
            right = partition_x - 1
        else:
            # We have partitioned too far to the left in nums1
            left = partition_x + 1
    
    # This should never be reached with valid sorted arrays
    raise ArrayOperationError("Unable to find median - arrays may not be properly sorted")


def _validate_array_contents(arr: List[Union[int, float]], name: str) -> None:
    """Validate that array contains only numeric values."""
    for i, val in enumerate(arr):
        if not isinstance(val, (int, float)) or val != val:  # Check for NaN
            raise ArrayOperationError(
                f"Array '{name}' contains invalid value at index {i}: {val}. "
                "Only integers and floats are allowed."
            )


def _validate_array_sorted(arr: List[Union[int, float]], name: str) -> None:
    """Validate that array is sorted in non-descending order."""
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            raise ArrayOperationError(
                f"Array '{name}' is not sorted. "
                f"Element at index {i} ({arr[i]}) is less than "
                f"element at index {i-1} ({arr[i-1]})"
            )


def _find_median_single_array(arr: List[Union[int, float]]) -> float:
    """Find median of a single sorted array."""
    n = len(arr)
    if n % 2 == 1:
        return float(arr[n // 2])
    else:
        mid1, mid2 = arr[n // 2 - 1], arr[n // 2]
        return float((mid1 + mid2) / 2.0)


def merge_sorted_arrays(nums1: List[Union[int, float]], 
                       nums2: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Merge two sorted arrays into one sorted array.
    
    This is a helper function that can be used for verification
    or when the merged array is needed.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        List: Merged sorted array
        
    Raises:
        ArrayOperationError: If input validation fails
    """
    if nums1 is None or nums2 is None:
        raise ArrayOperationError("Input arrays cannot be None")
    
    _validate_array_contents(nums1, "nums1")
    _validate_array_contents(nums2, "nums2")
    _validate_array_sorted(nums1, "nums1")
    _validate_array_sorted(nums2, "nums2")
    
    merged = []
    i = j = 0
    
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1
    
    # Add remaining elements
    merged.extend(nums1[i:])
    merged.extend(nums2[j:])
    
    return merged