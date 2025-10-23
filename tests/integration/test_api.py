"""
Integration tests for the Tornado application.

This module contains integration tests that test the complete flow
from HTTP request to response, including all layers of the application.
"""

import json
import asyncio
import pytest
from unittest.mock import patch, MagicMock

import tornado.testing
from tornado.web import Application
from tornado.httpclient import HTTPResponse

from app.routes import get_url_patterns
from app.utils.array_operations import ArrayOperationError


class TestMedianAPI(tornado.testing.AsyncHTTPTestCase):
    """Integration tests for median calculation API endpoints."""
    
    def get_app(self):
        """Create Tornado application for testing."""
        return Application(get_url_patterns(), debug=True)
    
    def test_median_calculation_success(self):
        """Test successful median calculation via API."""
        body = json.dumps({
            "nums1": [1, 3, 5],
            "nums2": [2, 4, 6]
        })
        
        response = self.fetch(
            '/api/v1/median',
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertEqual(data['median'], 3.5)
        self.assertEqual(data['array1_size'], 3)
        self.assertEqual(data['array2_size'], 3)
        self.assertEqual(data['total_elements'], 6)
        self.assertIn('execution_time_ms', data)
        self.assertGreater(data['execution_time_ms'], 0)
    
    def test_median_calculation_empty_body(self):
        """Test API with empty request body."""
        response = self.fetch(
            '/api/v1/median',
            method='POST',
            body='',
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 400)
        
        data = json.loads(response.body)
        self.assertIn('error', data)
        self.assertEqual(data['error_code'], 'BAD_REQUEST')
    
    def test_median_calculation_invalid_json(self):
        """Test API with invalid JSON."""
        response = self.fetch(
            '/api/v1/median',
            method='POST',
            body='{"invalid": json}',
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 400)
        
        data = json.loads(response.body)
        self.assertIn('error', data)
        self.assertEqual(data['error_code'], 'BAD_REQUEST')
    
    def test_median_calculation_validation_error(self):
        """Test API with validation errors."""
        # Missing required field
        body = json.dumps({"nums1": [1, 2, 3]})
        
        response = self.fetch(
            '/api/v1/median',
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 422)
        
        data = json.loads(response.body)
        self.assertEqual(data['error_code'], 'VALIDATION_ERROR')
        self.assertIn('details', data)
    
    def test_median_calculation_unsorted_array(self):
        """Test API with unsorted arrays."""
        body = json.dumps({
            "nums1": [3, 1, 2],  # Unsorted
            "nums2": [4, 5, 6]
        })
        
        response = self.fetch(
            '/api/v1/median',
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 422)
        
        data = json.loads(response.body)
        self.assertEqual(data['error_code'], 'VALIDATION_ERROR')
    
    def test_median_calculation_with_floats(self):
        """Test API with floating point numbers."""
        body = json.dumps({
            "nums1": [1.1, 2.2, 3.3],
            "nums2": [1.5, 2.5, 3.5]
        })
        
        response = self.fetch(
            '/api/v1/median',
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertAlmostEqual(data['median'], 2.35, places=2)
    
    def test_cors_headers(self):
        """Test that CORS headers are set correctly."""
        response = self.fetch('/api/v1/median', method='OPTIONS')
        
        self.assertEqual(response.code, 204)
        
        headers = response.headers
        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
        self.assertIn('Content-Type', headers['Access-Control-Allow-Headers'])
        self.assertIn('POST', headers['Access-Control-Allow-Methods'])
    
    def test_method_not_allowed(self):
        """Test unsupported HTTP methods."""
        response = self.fetch('/api/v1/median', method='GET')
        self.assertEqual(response.code, 405)
        
        response = self.fetch('/api/v1/median', method='PUT', body='{}')
        self.assertEqual(response.code, 405)


class TestMedianStatsAPI(tornado.testing.AsyncHTTPTestCase):
    """Integration tests for median statistics API endpoints."""
    
    def get_app(self):
        """Create Tornado application for testing."""
        return Application(get_url_patterns(), debug=True)
    
    def test_get_statistics(self):
        """Test getting median calculation statistics."""
        response = self.fetch('/api/v1/median/stats')
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertIn('total_calls', data)
        self.assertIn('total_execution_time_ms', data)
        self.assertIn('average_execution_time_ms', data)
        self.assertIn('service_status', data)
        self.assertEqual(data['service_status'], 'active')
    
    def test_reset_statistics(self):
        """Test resetting statistics."""
        response = self.fetch('/api/v1/median/stats', method='DELETE')
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertIn('message', data)
        self.assertIn('reset', data['message'].lower())


class TestMedianBatchAPI(tornado.testing.AsyncHTTPTestCase):
    """Integration tests for batch median calculation API."""
    
    def get_app(self):
        """Create Tornado application for testing."""
        return Application(get_url_patterns(), debug=True)
    
    def test_batch_calculation_success(self):
        """Test successful batch median calculation."""
        body = json.dumps({
            "calculations": [
                {"nums1": [1, 3], "nums2": [2, 4]},
                {"nums1": [1, 2], "nums2": [3, 4, 5]}
            ]
        })
        
        response = self.fetch(
            '/api/v1/median/batch',
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertEqual(data['total_calculations'], 2)
        self.assertEqual(data['successful_calculations'], 2)
        self.assertEqual(data['failed_calculations'], 0)
        self.assertEqual(len(data['results']), 2)
        
        # Check first result
        result1 = data['results'][0]
        self.assertEqual(result1['median'], 2.5)
        self.assertEqual(result1['status'], 'success')
        
        # Check second result  
        result2 = data['results'][1]
        self.assertEqual(result2['median'], 3.0)
        self.assertEqual(result2['status'], 'success')
    
    def test_batch_calculation_partial_failure(self):
        """Test batch calculation with some failures."""
        body = json.dumps({
            "calculations": [
                {"nums1": [1, 3], "nums2": [2, 4]},  # Valid
                {"nums1": [3, 1], "nums2": [2, 4]}   # Invalid (unsorted)
            ]
        })
        
        response = self.fetch(
            '/api/v1/median/batch',
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertEqual(data['total_calculations'], 2)
        self.assertEqual(data['successful_calculations'], 1)
        self.assertEqual(data['failed_calculations'], 1)
        
        # Check results
        results = data['results']
        success_result = next(r for r in results if r['status'] == 'success')
        error_result = next(r for r in results if r['status'] == 'error')
        
        self.assertEqual(success_result['median'], 2.5)
        self.assertIn('error_message', error_result)
    
    def test_batch_size_limit(self):
        """Test batch size limit enforcement."""
        # Create a batch that's too large
        calculations = [{"nums1": [1], "nums2": [2]} for _ in range(101)]
        body = json.dumps({"calculations": calculations})
        
        response = self.fetch(
            '/api/v1/median/batch',
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 422)
        
        data = json.loads(response.body)
        self.assertEqual(data['error_code'], 'BATCH_SIZE_ERROR')
    
    def test_batch_invalid_request(self):
        """Test batch API with invalid request format."""
        body = json.dumps({"invalid": "format"})
        
        response = self.fetch(
            '/api/v1/median/batch',
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 422)
        
        data = json.loads(response.body)
        self.assertEqual(data['error_code'], 'VALIDATION_ERROR')


class TestHealthAPI(tornado.testing.AsyncHTTPTestCase):
    """Integration tests for health check API endpoints."""
    
    def get_app(self):
        """Create Tornado application for testing."""
        return Application(get_url_patterns(), debug=True)
    
    def test_health_check(self):
        """Test basic health check endpoint."""
        response = self.fetch('/health')
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertIn('version', data)
        self.assertIn('uptime_seconds', data)
    
    def test_status_check(self):
        """Test detailed status endpoint."""
        response = self.fetch('/status')
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('dependencies', data)
        self.assertIn('service_stats', data)
        
        # Check dependencies
        deps = data['dependencies']
        self.assertIn('array_operations_util', deps)
        self.assertIn('logging_system', deps)
        self.assertIn('configuration', deps)
    
    def test_readiness_check(self):
        """Test readiness probe endpoint."""
        response = self.fetch('/ready')
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertEqual(data['status'], 'ready')
    
    def test_liveness_check(self):
        """Test liveness probe endpoint."""
        response = self.fetch('/live')
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertEqual(data['status'], 'alive')
    
    def test_alternative_health_endpoints(self):
        """Test alternative health check endpoint paths."""
        endpoints = ['/healthz', '/readyz', '/livez', '/health/ready', '/health/live']
        
        for endpoint in endpoints:
            response = self.fetch(endpoint)
            self.assertIn(response.code, [200, 503])  # Should return valid status
    
    @patch('app.routes.health_handlers.find_median_sorted_arrays')
    def test_liveness_check_failure(self, mock_median):
        """Test liveness check when basic functionality fails."""
        # Make the basic functionality test fail
        mock_median.side_effect = Exception("Test failure")
        
        response = self.fetch('/live')
        
        self.assertEqual(response.code, 503)
        
        data = json.loads(response.body)
        self.assertEqual(data['status'], 'not_alive')
        self.assertIn('error', data)


class TestErrorHandling(tornado.testing.AsyncHTTPTestCase):
    """Integration tests for error handling across the application."""
    
    def get_app(self):
        """Create Tornado application for testing."""
        return Application(get_url_patterns(), debug=True)
    
    def test_404_error(self):
        """Test 404 error handling."""
        response = self.fetch('/nonexistent')
        
        self.assertEqual(response.code, 404)
        
        data = json.loads(response.body)
        self.assertEqual(data['error_code'], 'NOT_FOUND')
        self.assertIn('timestamp', data)
    
    @patch('app.services.median_service.find_median_sorted_arrays')
    def test_internal_error_handling(self, mock_median):
        """Test internal error handling."""
        # Make the service throw an unexpected error
        mock_median.side_effect = Exception("Unexpected error")
        
        body = json.dumps({"nums1": [1, 2], "nums2": [3, 4]})
        response = self.fetch(
            '/api/v1/median',
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.code, 500)
        
        data = json.loads(response.body)
        self.assertEqual(data['error_code'], 'INTERNAL_ERROR')
    
    def test_content_type_validation(self):
        """Test content type validation."""
        response = self.fetch(
            '/api/v1/median',
            method='POST',
            body='{"nums1": [1, 2], "nums2": [3, 4]}',
            headers={'Content-Type': 'text/plain'}  # Wrong content type
        )
        
        # Should still work as we parse body regardless of content type
        # But in a stricter implementation, this might return an error
        self.assertIn(response.code, [200, 400, 415])


if __name__ == '__main__':
    import unittest
    unittest.main()