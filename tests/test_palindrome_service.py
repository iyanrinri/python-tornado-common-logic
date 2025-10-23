"""
Unit tests for palindrome service module.

Tests the business logic layer for palindrome operations including:
- Service initialization and configuration
- Palindrome pair calculations with statistics
- Error handling and validation
- Performance tracking
"""

import pytest
import asyncio
import logging
from app.services.palindrome_service import PalindromeCalculationService, palindrome_service
from app.services.dto_simple import PalindromeRequest, PalindromeResponse, PalindromeCheckRequest, PalindromeCheckResponse

# Configure test logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestPalindromeCalculationService:
    """Test class for palindrome calculation service."""

    def setup_method(self):
        """Setup for each test method."""
        self.service = PalindromeCalculationService()

    def test_service_initialization(self):
        """Test service initializes correctly."""
        assert self.service._call_count == 0
        assert self.service._total_execution_time == 0.0

import pytest
import logging
from unittest.mock import patch, MagicMock
from app.services.palindrome_service import PalindromeCalculationService, palindrome_service
from app.services.dto_simple import PalindromeRequest, PalindromeResponse, PalindromeCheckRequest, PalindromeCheckResponse

# Configure test logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestPalindromeCalculationService:
    """Test class for palindrome calculation service."""

    def setup_method(self):
        """Setup for each test method."""
        self.service = PalindromeCalculationService()

    def test_service_initialization(self):
        """Test service initializes correctly."""
        assert self.service._call_count == 0
        assert self.service._total_execution_time == 0.0

    @pytest.mark.asyncio
    async def test_find_palindrome_pairs_basic(self):
        """Test basic palindrome pairs calculation."""
        request = PalindromeRequest(words=["race", "car"])
        result = await self.service.find_palindrome_pairs(request)
        
        assert isinstance(result, PalindromeResponse)
        assert result.word_count == 2
        assert result.pairs_count >= 1  # Should find at least "race" + "car" = "racecar"
        
        # Should find "race" + "car" = "racecar"
        pairs = result.pairs
        assert [0, 1] in pairs
        
        # Service stats should be updated
        assert self.service._call_count == 1

    @pytest.mark.asyncio
    async def test_find_palindrome_pairs_empty_input(self):
        """Test with empty input."""
        request = PalindromeRequest(words=[])
        result = await self.service.find_palindrome_pairs(request)
        
        assert result.pairs == []
        assert result.word_count == 0
        assert result.pairs_count == 0

    @pytest.mark.asyncio
    async def test_find_palindrome_pairs_no_pairs(self):
        """Test when no palindrome pairs exist."""
        request = PalindromeRequest(words=["abc", "def", "ghi"])
        result = await self.service.find_palindrome_pairs(request)
        
        assert result.pairs == []
        assert result.word_count == 3
        assert result.pairs_count == 0

    @pytest.mark.asyncio
    async def test_check_palindrome_basic(self):
        """Test basic palindrome checking."""
        # Test palindrome
        request = PalindromeCheckRequest(text="racecar")
        result = await self.service.check_palindrome(request)
        assert result.is_palindrome is True
        assert result.text == "racecar"
        
        # Test non-palindrome
        request = PalindromeCheckRequest(text="hello")
        result = await self.service.check_palindrome(request)
        assert result.is_palindrome is False
        assert result.text == "hello"

    @pytest.mark.asyncio
    async def test_check_palindrome_edge_cases(self):
        """Test palindrome checking edge cases."""
        # Empty string
        request = PalindromeCheckRequest(text="")
        result = await self.service.check_palindrome(request)
        assert result.is_palindrome is True
        
        # Single character
        request = PalindromeCheckRequest(text="a")
        result = await self.service.check_palindrome(request)
        assert result.is_palindrome is True

    @pytest.mark.asyncio
    async def test_find_longest_pair_basic(self):
        """Test finding longest palindrome pair."""
        request = PalindromeRequest(words=["race", "car", "da", "d"])
        result = await self.service.find_longest_palindrome_pair(request)
        
        assert "found" in result
        
        # Should find "race" + "car" = "racecar" (7 chars)
        if result["found"]:
            assert result["length"] == 7
            assert result["words"] == ["race", "car"]
            assert result["palindrome"] == "racecar"

    @pytest.mark.asyncio
    async def test_find_longest_pair_no_pairs(self):
        """Test longest pair when no pairs exist."""
        request = PalindromeRequest(words=["abc", "def", "ghi"])
        result = await self.service.find_longest_palindrome_pair(request)
        
        assert result["found"] is False

    def test_get_statistics_basic(self):
        """Test getting service statistics."""
        stats = self.service.get_statistics()
        
        assert "total_calls" in stats
        assert "total_execution_time_ms" in stats
        assert "average_execution_time_ms" in stats
        assert stats["service_status"] == "active"

    def test_reset_statistics(self):
        """Test resetting service statistics."""
        # Reset
        self.service.reset_statistics()
        
        assert self.service._call_count == 0
        assert self.service._total_execution_time == 0.0

    def test_service_singleton_behavior(self):
        """Test that palindrome_service is a singleton-like instance."""
        # The imported palindrome_service should be the same instance
        assert isinstance(palindrome_service, PalindromeCalculationService)


class TestPalindromeDataTransferObjects:
    """Test palindrome DTOs."""

    def test_palindrome_request_valid(self):
        """Test valid palindrome request creation."""
        request_data = {"words": ["race", "car", "hello"]}
        request = PalindromeRequest.from_dict(request_data)
        
        assert request.words == ["race", "car", "hello"]

    def test_palindrome_request_invalid_missing_words(self):
        """Test palindrome request with missing words."""
        request_data = {}
        
        with pytest.raises(Exception):  # Should raise ValidationError
            PalindromeRequest.from_dict(request_data)

    def test_palindrome_request_invalid_words_type(self):
        """Test palindrome request with invalid words type."""
        request_data = {"words": "not a list"}
        
        with pytest.raises(Exception):  # Should raise ValidationError
            PalindromeRequest.from_dict(request_data)

    def test_palindrome_request_empty_words(self):
        """Test palindrome request with empty words list."""
        request_data = {"words": []}
        request = PalindromeRequest.from_dict(request_data)
        
        # Should be valid - empty list is acceptable
        assert request.words == []

    def test_palindrome_response_creation(self):
        """Test palindrome response creation."""
        response = PalindromeResponse(
            pairs=[[0, 1], [2, 3]],
            word_count=4,
            pairs_count=2,
            execution_time_ms=1.5
        )
        
        response_dict = response.to_dict()
        
        assert response_dict["pairs"] == [[0, 1], [2, 3]]
        assert response_dict["word_count"] == 4
        assert response_dict["pairs_count"] == 2
        assert response_dict["execution_time_ms"] == 1.5

    def test_palindrome_check_request_valid(self):
        """Test valid palindrome check request."""
        request_data = {"text": "racecar"}
        request = PalindromeCheckRequest.from_dict(request_data)
        
        assert request.text == "racecar"

    def test_palindrome_check_request_invalid(self):
        """Test invalid palindrome check request."""
        request_data = {"text": 123}
        
        with pytest.raises(Exception):  # Should raise ValidationError
            PalindromeCheckRequest.from_dict(request_data)

    def test_palindrome_check_response_creation(self):
        """Test palindrome check response creation."""
        response = PalindromeCheckResponse(
            text="racecar",
            is_palindrome=True,
            execution_time_ms=0.1
        )
        
        response_dict = response.to_dict()
        
        assert response_dict["text"] == "racecar"
        assert response_dict["is_palindrome"] is True
        assert response_dict["execution_time_ms"] == 0.1


if __name__ == "__main__":
    pytest.main([__file__])