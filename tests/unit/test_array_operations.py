"""
Unit tests for array operations utilities.

This module contains comprehensive tests for the array operations utility functions,
including edge cases, error conditions, and performance validation.
"""

import pytest
import math
from unittest.mock import patch, MagicMock

from app.utils.array_operations import (
    find_median_sorted_arrays,
    merge_sorted_arrays, 
    ArrayOperationError,
    _validate_array_contents,
    _validate_array_sorted,
    _find_median_single_array
)


class TestFindMedianSortedArrays:
    """Test cases for find_median_sorted_arrays function."""
    
    def test_basic_functionality(self):
        """Test basic median calculation scenarios."""
        # Test case 1: Even total length
        assert find_median_sorted_arrays([1, 3], [2]) == 2.0
        
        # Test case 2: Odd total length
        assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5
        
        # Test case 3: Same size arrays
        assert find_median_sorted_arrays([1, 3, 5], [2, 4, 6]) == 3.5
    
    def test_empty_arrays(self):
        """Test handling of empty arrays."""
        # One empty array
        assert find_median_sorted_arrays([], [1]) == 1.0
        assert find_median_sorted_arrays([1], []) == 1.0
        assert find_median_sorted_arrays([], [1, 2, 3]) == 2.0
        
        # Both empty arrays should raise error
        with pytest.raises(ArrayOperationError, match="Both arrays cannot be empty"):
            find_median_sorted_arrays([], [])
    
    def test_single_elements(self):
        """Test arrays with single elements."""
        assert find_median_sorted_arrays([1], [2]) == 1.5
        assert find_median_sorted_arrays([5], [1]) == 3.0
        assert find_median_sorted_arrays([0], [0]) == 0.0
    
    def test_negative_numbers(self):
        """Test arrays containing negative numbers."""
        assert find_median_sorted_arrays([-3, -1], [-2, 0]) == -1.5
        assert find_median_sorted_arrays([-5, -3, -1], [-4, -2]) == -3.0
        assert find_median_sorted_arrays([-10], [10]) == 0.0
    
    def test_floating_point_numbers(self):
        """Test arrays containing floating point numbers."""
        assert find_median_sorted_arrays([1.1, 2.2], [1.5, 3.3]) == 1.85
        assert find_median_sorted_arrays([0.5], [1.5, 2.5]) == 1.5
    
    def test_duplicate_values(self):
        """Test arrays with duplicate values."""
        assert find_median_sorted_arrays([1, 1], [1, 2]) == 1.0
        assert find_median_sorted_arrays([1, 2, 2], [2, 3, 4]) == 2.0
        assert find_median_sorted_arrays([5, 5, 5], [5, 5, 5]) == 5.0
    
    def test_large_arrays(self):
        """Test with larger arrays."""
        nums1 = list(range(0, 1000, 2))  # Even numbers 0-998
        nums2 = list(range(1, 1000, 2))  # Odd numbers 1-999
        result = find_median_sorted_arrays(nums1, nums2)
        assert result == 499.5
    
    def test_different_sizes(self):
        """Test arrays of very different sizes."""
        small = [1]
        large = list(range(2, 102))  # 2-101
        result = find_median_sorted_arrays(small, large)
        assert result == 51.5  # Median of combined array [1, 2, 3, ..., 101]
    
    def test_none_input(self):
        """Test None input validation."""
        with pytest.raises(ArrayOperationError, match="Input arrays cannot be None"):
            find_median_sorted_arrays(None, [1, 2])
        
        with pytest.raises(ArrayOperationError, match="Input arrays cannot be None"):
            find_median_sorted_arrays([1, 2], None)
    
    def test_invalid_array_contents(self):
        """Test validation of array contents."""
        # String in array
        with pytest.raises(ArrayOperationError, match="contains invalid value"):
            find_median_sorted_arrays([1, "2"], [3, 4])
        
        # NaN value
        with pytest.raises(ArrayOperationError, match="contains invalid value"):
            find_median_sorted_arrays([1, float('nan')], [3, 4])
        
        # None value in array
        with pytest.raises(ArrayOperationError, match="contains invalid value"):
            find_median_sorted_arrays([1, None], [3, 4])
    
    def test_unsorted_arrays(self):
        """Test validation of array sorting."""
        with pytest.raises(ArrayOperationError, match="not sorted"):
            find_median_sorted_arrays([3, 1, 2], [4, 5, 6])
        
        with pytest.raises(ArrayOperationError, match="not sorted"):
            find_median_sorted_arrays([1, 2, 3], [6, 4, 5])


class TestMergeSortedArrays:
    """Test cases for merge_sorted_arrays function."""
    
    def test_basic_merge(self):
        """Test basic array merging."""
        result = merge_sorted_arrays([1, 3, 5], [2, 4, 6])
        assert result == [1, 2, 3, 4, 5, 6]
    
    def test_empty_arrays_merge(self):
        """Test merging with empty arrays."""
        assert merge_sorted_arrays([], [1, 2, 3]) == [1, 2, 3]
        assert merge_sorted_arrays([1, 2, 3], []) == [1, 2, 3]
        assert merge_sorted_arrays([], []) == []
    
    def test_merge_with_duplicates(self):
        """Test merging arrays with duplicate values."""
        result = merge_sorted_arrays([1, 2, 2], [2, 3, 4])
        assert result == [1, 2, 2, 2, 3, 4]
    
    def test_merge_validation_errors(self):
        """Test that merge function validates inputs properly."""
        with pytest.raises(ArrayOperationError):
            merge_sorted_arrays(None, [1, 2])
        
        with pytest.raises(ArrayOperationError):
            merge_sorted_arrays([2, 1], [3, 4])  # Unsorted


class TestValidationFunctions:
    """Test cases for validation helper functions."""
    
    def test_validate_array_contents(self):
        """Test array contents validation."""
        # Valid arrays should not raise
        _validate_array_contents([1, 2, 3], "test")
        _validate_array_contents([1.1, 2.2, 3.3], "test")
        _validate_array_contents([-1, 0, 1], "test")
        _validate_array_contents([], "test")
        
        # Invalid arrays should raise
        with pytest.raises(ArrayOperationError):
            _validate_array_contents([1, "2"], "test")
        
        with pytest.raises(ArrayOperationError):
            _validate_array_contents([1, None], "test")
        
        with pytest.raises(ArrayOperationError):
            _validate_array_contents([1, float('nan')], "test")
    
    def test_validate_array_sorted(self):
        """Test array sorting validation."""
        # Sorted arrays should not raise
        _validate_array_sorted([1, 2, 3], "test")
        _validate_array_sorted([1, 1, 2], "test")  # Equal elements allowed
        _validate_array_sorted([], "test")
        _validate_array_sorted([1], "test")
        
        # Unsorted arrays should raise
        with pytest.raises(ArrayOperationError):
            _validate_array_sorted([3, 1, 2], "test")
        
        with pytest.raises(ArrayOperationError):
            _validate_array_sorted([1, 3, 2], "test")
    
    def test_find_median_single_array(self):
        """Test single array median calculation."""
        # Odd length
        assert _find_median_single_array([1, 2, 3]) == 2.0
        assert _find_median_single_array([5]) == 5.0
        
        # Even length
        assert _find_median_single_array([1, 2, 3, 4]) == 2.5
        assert _find_median_single_array([1, 3]) == 2.0


class TestPerformance:
    """Test cases for performance characteristics."""
    
    def test_large_arrays_performance(self):
        """Test performance with large arrays."""
        import time
        
        # Create large sorted arrays
        nums1 = list(range(0, 10000, 2))
        nums2 = list(range(1, 10000, 2))
        
        start_time = time.perf_counter()
        result = find_median_sorted_arrays(nums1, nums2)
        end_time = time.perf_counter()
        
        execution_time = (end_time - start_time) * 1000  # Convert to ms
        
        # Should complete in reasonable time (< 10ms for this size)
        assert execution_time < 10
        assert result == 4999.5
    
    @patch('app.utils.array_operations.logger')
    def test_logging_calls(self, mock_logger):
        """Test that appropriate logging calls are made."""
        find_median_sorted_arrays([1, 3], [2, 4])
        
        # Verify debug logging was called
        mock_logger.debug.assert_called()
        
        # Check specific log messages
        calls = [call[0][0] for call in mock_logger.debug.call_args_list]
        assert any("Finding median for arrays of size" in call for call in calls)
        assert any("Calculated median:" in call for call in calls)


class TestEdgeCases:
    """Test cases for edge cases and boundary conditions."""
    
    def test_extreme_values(self):
        """Test with extreme numeric values."""
        # Very large numbers
        large_nums1 = [1e10, 2e10]
        large_nums2 = [1.5e10, 3e10]
        result = find_median_sorted_arrays(large_nums1, large_nums2)
        assert result == 1.75e10
        
        # Very small numbers
        small_nums1 = [1e-10, 2e-10]
        small_nums2 = [1.5e-10, 3e-10]
        result = find_median_sorted_arrays(small_nums1, small_nums2)
        assert abs(result - 1.75e-10) < 1e-15  # Account for floating point precision
    
    def test_infinite_values(self):
        """Test handling of infinite values."""
        # Positive infinity
        result = find_median_sorted_arrays([1, 2], [3, float('inf')])
        assert result == 2.5
        
        # Negative infinity  
        result = find_median_sorted_arrays([float('-inf'), 1], [2, 3])
        assert result == 1.5
    
    def test_precision_edge_cases(self):
        """Test floating point precision edge cases."""
        # Numbers very close together
        nums1 = [1.0000000001, 1.0000000002]
        nums2 = [1.0000000001, 1.0000000003]
        result = find_median_sorted_arrays(nums1, nums2)
        expected = (1.0000000001 + 1.0000000002) / 2
        assert abs(result - expected) < 1e-15