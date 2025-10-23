"""
Utility package for common operations.

This package contains utility functions and classes used across the application.
"""

from .array_operations import find_median_sorted_arrays, merge_sorted_arrays, ArrayOperationError
from .palindrome_operations import (
    find_palindrome_pairs, 
    find_palindrome_pairs_naive, 
    is_palindrome, 
    is_palindrome_optimized,
    get_palindrome_statistics,
    find_longest_palindrome_pair,
    PalindromeOperationError
)

__all__ = [
    'find_median_sorted_arrays', 
    'merge_sorted_arrays', 
    'ArrayOperationError',
    'find_palindrome_pairs',
    'find_palindrome_pairs_naive',
    'is_palindrome',
    'is_palindrome_optimized', 
    'get_palindrome_statistics',
    'find_longest_palindrome_pair',
    'PalindromeOperationError'
]