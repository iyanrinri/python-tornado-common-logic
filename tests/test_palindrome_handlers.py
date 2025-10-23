"""
Integration tests for palindrome API handlers.

Tests the REST API endpoints for palindrome operations including:
- Palindrome pairs calculation endpoint
- Palindrome checking endpoint
- Longest pair endpoint
- Statistics endpoint
- Batch operations endpoint
"""

import pytest
import json
import asyncio
from unittest.mock import patch, MagicMock
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from app.routes.palindrome_handlers import (
    PalindromeHandler,
    PalindromeCheckHandler, 
    PalindromeLongestHandler,
    PalindromeStatsHandler,
    PalindromeBatchHandler
)


class TestPalindromeAPIHandlers(AsyncHTTPTestCase):
    """Test class for palindrome API handlers."""

    def get_app(self):
        """Create test application with palindrome handlers."""
        return Application([
            (r"/api/v1/palindrome/pairs", PalindromeHandler),
            (r"/api/v1/palindrome/check", PalindromeCheckHandler),
            (r"/api/v1/palindrome/longest", PalindromeLongestHandler),
            (r"/api/v1/palindrome/stats", PalindromeStatsHandler),
            (r"/api/v1/palindrome/batch", PalindromeBatchHandler),
        ])

    def test_palindrome_pairs_endpoint_success(self):
        """Test successful palindrome pairs calculation."""
        body = json.dumps({"words": ["race", "car"]})
        response = self.fetch(
            "/api/v1/palindrome/pairs",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertIn("pairs", data)
        self.assertIn("word_count", data)
        self.assertIn("pairs_count", data)
        self.assertEqual(data["word_count"], 2)

    def test_palindrome_pairs_endpoint_empty_list(self):
        """Test palindrome pairs with empty list."""
        body = json.dumps({"words": []})
        response = self.fetch(
            "/api/v1/palindrome/pairs",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertEqual(data["pairs"], [])
        self.assertEqual(data["word_count"], 0)
        self.assertEqual(data["pairs_count"], 0)

    def test_palindrome_pairs_endpoint_invalid_json(self):
        """Test palindrome pairs with invalid JSON."""
        body = "invalid json"
        response = self.fetch(
            "/api/v1/palindrome/pairs",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.code, 400)
        
        data = json.loads(response.body)
        self.assertIn("error", data)
        self.assertIn("error_code", data)

    def test_palindrome_pairs_endpoint_missing_words(self):
        """Test palindrome pairs with missing words field."""
        body = json.dumps({"invalid": "field"})
        response = self.fetch(
            "/api/v1/palindrome/pairs",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.code, 422)
        
        data = json.loads(response.body)
        self.assertIn("error", data)
        self.assertEqual(data["error_code"], "VALIDATION_ERROR")

    def test_palindrome_check_endpoint_success(self):
        """Test successful palindrome checking."""
        body = json.dumps({"text": "racecar"})
        response = self.fetch(
            "/api/v1/palindrome/check",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertIn("text", data)
        self.assertIn("is_palindrome", data)
        self.assertEqual(data["text"], "racecar")
        self.assertTrue(data["is_palindrome"])

    def test_palindrome_check_endpoint_not_palindrome(self):
        """Test palindrome checking with non-palindrome."""
        body = json.dumps({"text": "hello"})
        response = self.fetch(
            "/api/v1/palindrome/check",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertEqual(data["text"], "hello")
        self.assertFalse(data["is_palindrome"])

    def test_longest_pair_endpoint_success(self):
        """Test successful longest palindrome pair finding."""
        body = json.dumps({"words": ["race", "car", "da", "d"]})
        response = self.fetch(
            "/api/v1/palindrome/longest",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertIn("found", data)
        
        if data["found"]:
            self.assertIn("palindrome", data)
            self.assertIn("length", data)
            self.assertIn("words", data)

    def test_longest_pair_endpoint_no_pairs(self):
        """Test longest pair endpoint when no pairs exist."""
        body = json.dumps({"words": ["abc", "def", "ghi"]})
        response = self.fetch(
            "/api/v1/palindrome/longest",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertFalse(data["found"])

    def test_stats_endpoint_get(self):
        """Test getting palindrome service statistics."""
        response = self.fetch("/api/v1/palindrome/stats", method="GET")
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertIn("total_calls", data)
        self.assertIn("service_status", data)

    def test_stats_endpoint_reset(self):
        """Test resetting palindrome service statistics."""
        response = self.fetch("/api/v1/palindrome/stats", method="DELETE")
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertIn("message", data)

    def test_batch_endpoint_success(self):
        """Test successful batch palindrome operations."""
        body = json.dumps({
            "operations": [
                {"words": ["race", "car"]},
                {"words": ["abc", "def"]}
            ]
        })
        response = self.fetch(
            "/api/v1/palindrome/batch",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertIn("results", data)
        self.assertIn("summary", data)
        self.assertEqual(len(data["results"]), 2)

    def test_batch_endpoint_empty_operations(self):
        """Test batch endpoint with empty operations."""
        body = json.dumps({"operations": []})
        response = self.fetch(
            "/api/v1/palindrome/batch",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.code, 200)
        
        data = json.loads(response.body)
        self.assertEqual(len(data["results"]), 0)

    def test_method_not_allowed(self):
        """Test method not allowed responses."""
        # GET on POST-only endpoints should return 405
        response = self.fetch("/api/v1/palindrome/pairs", method="GET")
        self.assertEqual(response.code, 405)

    def test_cors_headers(self):
        """Test CORS headers in responses."""
        body = json.dumps({"words": ["race", "car"]})
        response = self.fetch(
            "/api/v1/palindrome/pairs",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        # Check for CORS headers
        headers = dict(response.headers)
        self.assertIn("Access-Control-Allow-Origin", headers)

    def test_content_type_headers(self):
        """Test content type headers in responses."""
        body = json.dumps({"words": ["race", "car"]})
        response = self.fetch(
            "/api/v1/palindrome/pairs",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        
        # Check content type
        headers = dict(response.headers)
        self.assertEqual(headers.get("Content-Type"), "application/json; charset=UTF-8")


if __name__ == "__main__":
    pytest.main([__file__])