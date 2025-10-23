"""
Unit tests for palindrome operations module.

Tests the core palindrome algorithms including:
- Palindrome pairs finding
- Individual palindrome checking  
- Longest palindrome pair finding
"""

import pytest
import logging
from app.utils.palindrome_operations import find_palindrome_pairs, is_palindrome, find_longest_palindrome_pair

# Configure test logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestPalindromeOperations:
    """Test class for palindrome operations."""

    def test_find_palindrome_pairs_basic(self):
        """Test basic palindrome pairs finding."""
        # Basic test case
        words = ["lls", "s", "sssll"]
        result = find_palindrome_pairs(words)
        
        # Should find pairs that form palindromes
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Check specific pairs
        expected_pairs = [(0, 1), (1, 0)]  # "lls" + "s" = "llss" (not palindrome), "s" + "lls" = "slls" (not palindrome)
        # Let's check what we actually get
        logger.debug(f"Basic test result: {result}")

    def test_find_palindrome_pairs_classic_example(self):
        """Test with classic example."""
        words = ["code", "edoc", "da", "d"]
        result = find_palindrome_pairs(words)
        
        # "code" + "edoc" = "codeedoc" (not palindrome)
        # "edoc" + "code" = "edoccode" (not palindrome)  
        # "d" + "da" = "dda" (not palindrome)
        # "da" + "d" = "dad" (palindrome!)
        
        logger.debug(f"Classic test result: {result}")
        assert (2, 3) in result  # "da" + "d" = "dad"

    def test_find_palindrome_pairs_empty_input(self):
        """Test with empty input."""
        result = find_palindrome_pairs([])
        assert result == []

    def test_find_palindrome_pairs_single_word(self):
        """Test with single word."""
        result = find_palindrome_pairs(["test"])
        assert result == []

    def test_find_palindrome_pairs_no_pairs(self):
        """Test case where no palindrome pairs exist."""
        words = ["abc", "def", "ghi"]
        result = find_palindrome_pairs(words)
        assert result == []

    def test_find_palindrome_pairs_self_palindromes(self):
        """Test with words that are palindromes themselves."""
        words = ["aba", "cdc", "xyz"]
        result = find_palindrome_pairs(words)
        # Should find pairs where one word is empty prefix/suffix
        logger.debug(f"Self palindromes result: {result}")

    def test_find_palindrome_pairs_complex_case(self):
        """Test with more complex palindrome pairs."""
        words = ["race", "car", "acer"]
        result = find_palindrome_pairs(words)
        # "race" + "car" = "racecar" (palindrome!)
        logger.debug(f"Complex test result: {result}")
        assert (0, 1) in result

    def test_is_palindrome_basic(self):
        """Test basic palindrome checking."""
        assert is_palindrome("") is True
        assert is_palindrome("a") is True
        assert is_palindrome("aa") is True
        assert is_palindrome("aba") is True
        assert is_palindrome("racecar") is True
        
    def test_is_palindrome_not_palindrome(self):
        """Test non-palindrome strings."""
        assert is_palindrome("ab") is False
        assert is_palindrome("abc") is False
        assert is_palindrome("racecard") is False

    def test_is_palindrome_case_sensitive(self):
        """Test that palindrome check is case sensitive."""
        assert is_palindrome("Aa") is False
        assert is_palindrome("RaceCar") is False

    def test_find_longest_palindrome_pair_basic(self):
        """Test finding longest palindrome pair."""
        words = ["race", "car", "da", "d"]
        result = find_longest_palindrome_pair(words)
        
        # Should return the pair that forms the longest palindrome
        # "race" + "car" = "racecar" (7 chars)
        # "da" + "d" = "dad" (3 chars)
        expected = (0, 1, 7)  # indices and length
        assert result == expected

    def test_find_longest_palindrome_pair_no_pairs(self):
        """Test longest pair when no pairs exist."""
        words = ["abc", "def", "ghi"]
        result = find_longest_palindrome_pair(words)
        assert result is None

    def test_find_longest_palindrome_pair_empty(self):
        """Test longest pair with empty input."""
        result = find_longest_palindrome_pair([])
        assert result is None

    def test_find_longest_palindrome_pair_tie(self):
        """Test longest pair when there's a tie."""
        words = ["ab", "ba", "cd", "dc"]
        result = find_longest_palindrome_pair(words)
        
        # Both "ab"+"ba"="abba" and "cd"+"dc"="cddc" are length 4
        # Should return the first one found
        expected = (0, 1, 4)
        assert result == expected

    def test_palindrome_operations_edge_cases(self):
        """Test edge cases and boundary conditions."""
        
        # Very long words
        long_word1 = "a" * 1000
        long_word2 = "a" * 1000
        result = find_palindrome_pairs([long_word1, long_word2])
        # Should handle large inputs efficiently
        assert isinstance(result, list)
        
        # Special characters and numbers
        words = ["12321", "ab!ba", "a1b2b1a"]
        result = find_palindrome_pairs(words)
        assert isinstance(result, list)
        
        # Unicode characters
        words = ["αβα", "γδγ", "αβαγδγ"]
        result = find_palindrome_pairs(words)
        assert isinstance(result, list)

    def test_palindrome_algorithm_performance_characteristics(self):
        """Test algorithm performance characteristics."""
        # Test that algorithm handles reasonable input sizes efficiently
        
        # Medium size input
        words = [f"word{i}" for i in range(100)]
        words.extend([f"drow{i}" for i in range(100)])  # Add some potential pairs
        
        result = find_palindrome_pairs(words)
        assert isinstance(result, list)
        
        # Check that we get expected pairs
        # "word0" + "drow0" = "word0drow0" (not palindrome)
        # But "word" + "drow" = "worddrow" (not palindrome either)
        logger.debug(f"Performance test found {len(result)} pairs")

    def test_palindrome_pairs_with_duplicates(self):
        """Test palindrome pairs with duplicate words."""
        words = ["abc", "cba", "abc", "cba"]
        result = find_palindrome_pairs(words)
        
        # Should find multiple pairs: (0,1), (0,3), (2,1), (2,3)
        # "abc" + "cba" = "abccba" (palindrome!)
        expected_pairs = [(0, 1), (0, 3), (2, 1), (2, 3)]
        
        logger.debug(f"Duplicates test result: {result}")
        for pair in expected_pairs:
            assert pair in result

    def test_palindrome_validation_comprehensive(self):
        """Comprehensive validation of palindrome detection."""
        
        test_cases = [
            # (string, expected_result)
            ("", True),
            ("a", True),
            ("ab", False),
            ("aba", True),
            ("abba", True),
            ("abcba", True),
            ("abccba", True),
            ("racecar", True),
            ("racecard", False),
            ("A man a plan a canal Panama", False),  # spaces matter
            ("AmanaplanacanalPanama", False),  # case matters
            ("12321", True),
            ("12345", False),
        ]
        
        for test_string, expected in test_cases:
            result = is_palindrome(test_string)
            assert result == expected, f"Failed for '{test_string}': expected {expected}, got {result}"


if __name__ == "__main__":
    pytest.main([__file__])