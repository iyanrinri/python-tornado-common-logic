"""
Utility package for common operations.

This package contains utility functions and classes used across the application.
"""

from .array_operations import find_median_sorted_arrays, merge_sorted_arrays, ArrayOperationError

__all__ = ['find_median_sorted_arrays', 'merge_sorted_arrays', 'ArrayOperationError']