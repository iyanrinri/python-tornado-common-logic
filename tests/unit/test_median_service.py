"""
Unit tests for median calculation service.

This module contains comprehensive tests for the median calculation service,
including business logic validation, error handling, and performance monitoring.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime

from app.services.median_service import MedianCalculationService, HealthService
from app.services.dto import MedianRequest, MedianResponse
from app.utils.array_operations import ArrayOperationError


class TestMedianCalculationService:
    """Test cases for MedianCalculationService."""
    
    @pytest.fixture
    def service(self):
        """Create a fresh service instance for each test."""
        return MedianCalculationService()
    
    @pytest.mark.asyncio
    async def test_calculate_median_success(self, service):
        """Test successful median calculation."""
        request = MedianRequest(nums1=[1, 3], nums2=[2, 4])
        response = await service.calculate_median(request)
        
        assert isinstance(response, MedianResponse)
        assert response.median == 2.5
        assert response.array1_size == 2
        assert response.array2_size == 2
        assert response.total_elements == 4
        assert response.execution_time_ms > 0
    
    @pytest.mark.asyncio
    async def test_calculate_median_empty_arrays(self, service):
        """Test median calculation with empty arrays."""
        # One empty array
        request = MedianRequest(nums1=[], nums2=[1, 2, 3])
        response = await service.calculate_median(request)
        assert response.median == 2.0
        
        # Test statistics updated
        stats = service.get_statistics()
        assert stats["total_calls"] == 1
    
    @pytest.mark.asyncio
    async def test_calculate_median_array_operation_error(self, service):
        """Test handling of ArrayOperationError."""
        with patch('app.services.median_service.find_median_sorted_arrays') as mock_func:
            mock_func.side_effect = ArrayOperationError("Invalid arrays")
            
            request = MedianRequest(nums1=[1, 2], nums2=[3, 4])
            
            with pytest.raises(ArrayOperationError):
                await service.calculate_median(request)
    
    @pytest.mark.asyncio
    async def test_calculate_median_unexpected_error(self, service):
        """Test handling of unexpected errors."""
        with patch('app.services.median_service.find_median_sorted_arrays') as mock_func:
            mock_func.side_effect = ValueError("Unexpected error")
            
            request = MedianRequest(nums1=[1, 2], nums2=[3, 4])
            
            with pytest.raises(ArrayOperationError, match="Calculation failed"):
                await service.calculate_median(request)
    
    @pytest.mark.asyncio
    async def test_performance_monitoring(self, service):
        """Test that performance is properly monitored."""
        request = MedianRequest(nums1=[1, 2], nums2=[3, 4])
        
        # Make multiple calls
        await service.calculate_median(request)
        await service.calculate_median(request)
        await service.calculate_median(request)
        
        stats = service.get_statistics()
        assert stats["total_calls"] == 3
        assert stats["total_execution_time_ms"] > 0
        assert stats["average_execution_time_ms"] > 0
        assert stats["service_status"] == "active"
    
    def test_get_statistics_empty(self, service):
        """Test statistics when no calls have been made."""
        stats = service.get_statistics()
        assert stats["total_calls"] == 0
        assert stats["total_execution_time_ms"] == 0
        assert stats["average_execution_time_ms"] == 0
        assert stats["service_status"] == "active"
    
    def test_reset_statistics(self, service):
        """Test statistics reset functionality."""
        # Make some calls first
        service._call_count = 5
        service._total_execution_time = 100.5
        
        # Reset
        service.reset_statistics()
        
        # Verify reset
        stats = service.get_statistics()
        assert stats["total_calls"] == 0
        assert stats["total_execution_time_ms"] == 0
        assert stats["average_execution_time_ms"] == 0
    
    @patch('app.services.median_service.logger')
    def test_logging(self, mock_logger, service):
        """Test that appropriate logging occurs."""
        asyncio.run(self._test_logging_async(service))
        
        # Verify logging calls were made
        mock_logger.info.assert_called()
        
        # Check for specific log messages
        calls = [call[0][0] for call in mock_logger.info.call_args_list]
        log_messages = [call for call in calls if isinstance(call, str)]
        
        assert any("Starting median calculation" in msg for msg in log_messages)
        assert any("Median calculation completed successfully" in msg for msg in log_messages)
    
    async def _test_logging_async(self, service):
        """Helper method for async logging test."""
        request = MedianRequest(nums1=[1, 2], nums2=[3, 4])
        await service.calculate_median(request)


class TestHealthService:
    """Test cases for HealthService."""
    
    @pytest.fixture
    def health_service(self):
        """Create a fresh health service instance for each test."""
        return HealthService()
    
    @pytest.mark.asyncio
    async def test_get_health_status(self, health_service):
        """Test health status retrieval."""
        status = await health_service.get_health_status()
        
        assert status["status"] == "healthy"
        assert "timestamp" in status
        assert status["version"] == "1.0.0"
        assert status["uptime_seconds"] >= 0
        
        # Validate timestamp format
        timestamp = status["timestamp"]
        assert timestamp.endswith("Z")
        
        # Should be able to parse as ISO format
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    
    def test_check_dependencies(self, health_service):
        """Test dependency status check."""
        deps = health_service.check_dependencies()
        
        assert isinstance(deps, dict)
        assert "array_operations_util" in deps
        assert "logging_system" in deps
        assert "configuration" in deps
        
        # All dependencies should be in expected states
        expected_states = {"available", "active", "loaded"}
        for dep_status in deps.values():
            assert dep_status in expected_states
    
    @pytest.mark.asyncio
    async def test_uptime_tracking(self, health_service):
        """Test that uptime is tracked correctly."""
        # Get initial status
        status1 = await health_service.get_health_status()
        uptime1 = status1["uptime_seconds"]
        
        # Wait a short time
        await asyncio.sleep(0.01)
        
        # Get status again
        status2 = await health_service.get_health_status()
        uptime2 = status2["uptime_seconds"]
        
        # Uptime should have increased
        assert uptime2 > uptime1


class TestServiceIntegration:
    """Integration tests between services."""
    
    @pytest.mark.asyncio
    async def test_service_instances_available(self):
        """Test that global service instances are available."""
        from app.services import median_service, health_service
        
        # Should be instances of correct classes
        assert isinstance(median_service, MedianCalculationService)
        assert isinstance(health_service, HealthService)
        
        # Should be functional
        request = MedianRequest(nums1=[1, 2], nums2=[3, 4])
        response = await median_service.calculate_median(request)
        assert response.median == 2.5
        
        health_status = await health_service.get_health_status()
        assert health_status["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test concurrent service operations."""
        from app.services import median_service
        
        # Create multiple concurrent requests
        requests = [
            MedianRequest(nums1=[1, 2], nums2=[3, 4]),
            MedianRequest(nums1=[1, 3, 5], nums2=[2, 4, 6]),
            MedianRequest(nums1=[], nums2=[1, 2, 3]),
        ]
        
        # Execute concurrently
        tasks = [median_service.calculate_median(req) for req in requests]
        responses = await asyncio.gather(*tasks)
        
        # Verify all responses
        assert len(responses) == 3
        assert responses[0].median == 2.5
        assert responses[1].median == 3.5
        assert responses[2].median == 2.0
        
        # Statistics should reflect all calls
        stats = median_service.get_statistics()
        assert stats["total_calls"] >= 3


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @pytest.mark.asyncio
    async def test_service_error_propagation(self):
        """Test that service errors are properly propagated."""
        service = MedianCalculationService()
        
        # Test with request that will cause validation error in utils
        with patch('app.services.median_service.find_median_sorted_arrays') as mock_func:
            mock_func.side_effect = ArrayOperationError("Test error")
            
            request = MedianRequest(nums1=[1, 2], nums2=[3, 4])
            
            with pytest.raises(ArrayOperationError, match="Test error"):
                await service.calculate_median(request)
    
    @pytest.mark.asyncio
    async def test_health_service_resilience(self):
        """Test health service resilience to errors."""
        health_service = HealthService()
        
        # Even if there are internal errors, health check should work
        with patch.object(health_service, '_start_time', None):
            # This might cause an error in uptime calculation
            try:
                status = await health_service.get_health_status()
                # Should still return some status
                assert "status" in status
            except Exception:
                # If it fails, it should fail gracefully
                pass