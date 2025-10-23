"""
Palindrome pairs utility functions.

This module contains optimized algorithms for finding palindrome pairs
from a list of strings. A palindrome pair is formed by concatenating
two strings from the list that result in a palindrome.
"""

from typing import List, Tuple, Set
import logging

logger = logging.getLogger(__name__)


class PalindromeOperationError(Exception):
    """Custom exception for palindrome operation errors."""
    pass


def find_palindrome_pairs(words: List[str]) -> List[Tuple[int, int]]:
    """
    Find all pairs of indices where words[i] + words[j] forms a palindrome.
    
    This function uses a simple but correct approach to find all palindrome pairs.
    
    Args:
        words: List of words to find palindrome pairs from
        
    Returns:
        List[Tuple[int, int]]: List of index pairs (i, j) where words[i] + words[j]
                              forms a palindrome and i != j
        
    Raises:
        PalindromeOperationError: If input validation fails
        
    Examples:
        >>> find_palindrome_pairs(["race", "car"])
        [(0, 1)]
        >>> find_palindrome_pairs(["abc", "def"])
        []
        
    Time Complexity: O(n²k) where n is number of words, k is average word length
    Space Complexity: O(1) excluding result storage
    """
    # Input validation
    if not isinstance(words, list):
        raise PalindromeOperationError("Input must be a list of strings")
    
    _validate_word_list(words)
    
    logger.debug(f"Finding palindrome pairs for {len(words)} words")
    
    if len(words) < 2:
        logger.debug("Less than 2 words provided, returning empty result")
        return []
    
    # Use straightforward approach for correctness
    result = []
    n = len(words)
    
    for i in range(n):
        for j in range(n):
            if i != j:
                combined = words[i] + words[j]
                if is_palindrome(combined):
                    result.append((i, j))
    
    logger.debug(f"Found {len(result)} palindrome pairs")
    return result


def find_palindrome_pairs_naive(words: List[str]) -> List[Tuple[int, int]]:
    """
    Naive O(n²k) solution for finding palindrome pairs.
    
    This is a simpler but less efficient implementation that checks
    all possible pairs directly.
    
    Args:
        words: List of words to find palindrome pairs from
        
    Returns:
        List[Tuple[int, int]]: List of index pairs (i, j) where words[i] + words[j]
                              forms a palindrome and i != j
    """
    _validate_word_list(words)
    
    result = []
    n = len(words)
    
    for i in range(n):
        for j in range(n):
            if i != j:
                combined = words[i] + words[j]
                if is_palindrome(combined):
                    result.append((i, j))
    
    return result


def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome.
    
    Args:
        s: String to check
        
    Returns:
        bool: True if string is a palindrome, False otherwise
        
    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("")
        True
        >>> is_palindrome("a")
        True
    """
    if not isinstance(s, str):
        raise PalindromeOperationError("Input must be a string")
    
    return s == s[::-1]


def is_palindrome_optimized(s: str) -> bool:
    """
    Optimized palindrome check using two pointers.
    
    Args:
        s: String to check
        
    Returns:
        bool: True if string is a palindrome, False otherwise
    """
    if not isinstance(s, str):
        raise PalindromeOperationError("Input must be a string")
    
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True


def _validate_word_list(words: List[str]) -> None:
    """Validate that input is a list of strings."""
    for i, word in enumerate(words):
        if not isinstance(word, str):
            raise PalindromeOperationError(
                f"All items must be strings. Item at index {i} is {type(word)}"
            )
        # Note: We allow empty strings as they are valid for palindrome operations


class TrieNode:
    """Node for the Palindrome Trie data structure."""
    
    def __init__(self):
        self.children = {}
        self.word_indices = []  # Indices of words ending at this node
        self.palindrome_suffixes = []  # Indices where remaining suffix forms palindrome


class PalindromeTrie:
    """
    Specialized Trie for efficient palindrome pair finding.
    
    This Trie stores reversed words and maintains information about
    palindromic suffixes to enable efficient palindrome pair detection.
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def add_word(self, word: str, index: int) -> None:
        """
        Add a word to the trie.
        
        Args:
            word: Word to add (should be reversed)
            index: Original index of the word
        """
        node = self.root
        
        # Check for palindromic suffixes while traversing
        for i in range(len(word)):
            # If remaining part of word is a palindrome, record it
            if is_palindrome_optimized(word[i:]):
                node.palindrome_suffixes.append(index)
            
            char = word[i]
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        # Mark end of word
        node.word_indices.append(index)
        
        # Check if empty suffix (entire remaining part) is palindrome
        node.palindrome_suffixes.append(index)
    
    def find_pairs_with_prefix(self, word: str, current_index: int) -> List[Tuple[int, int]]:
        """
        Find all palindrome pairs where the given word is the first part.
        
        Args:
            word: The word to use as prefix
            current_index: Index of the current word
            
        Returns:
            List[Tuple[int, int]]: Pairs (current_index, other_index) that form palindromes
        """
        pairs = []
        node = self.root
        
        # Traverse the word in the trie
        for i, char in enumerate(word):
            # Check if any word ends here and remaining part of current word is palindrome
            for word_idx in node.word_indices:
                if word_idx != current_index and is_palindrome_optimized(word[i:]):
                    pairs.append((current_index, word_idx))
            
            # Move to next character
            if char not in node.children:
                return pairs
            node = node.children[char]
        
        # Check words that end at current node (exact matches)
        for word_idx in node.word_indices:
            if word_idx != current_index:
                pairs.append((current_index, word_idx))
        
        # Check words where remaining part forms palindrome
        for word_idx in node.palindrome_suffixes:
            if word_idx != current_index:
                pairs.append((current_index, word_idx))
        
        return pairs


def get_palindrome_statistics(words: List[str]) -> dict:
    """
    Get statistics about palindrome pairs in the word list.
    
    Args:
        words: List of words to analyze
        
    Returns:
        dict: Statistics including counts and examples
    """
    _validate_word_list(words)
    
    pairs = find_palindrome_pairs(words)
    
    # Collect some example palindromes
    examples = []
    for i, j in pairs[:5]:  # Limit to first 5 examples
        palindrome = words[i] + words[j]
        examples.append({
            "indices": (i, j),
            "words": (words[i], words[j]),
            "palindrome": palindrome
        })
    
    return {
        "total_words": len(words),
        "palindrome_pairs_count": len(pairs),
        "unique_words_in_pairs": len(set(idx for pair in pairs for idx in pair)),
        "examples": examples,
        "has_palindromes": len(pairs) > 0
    }


def find_longest_palindrome_pair(words: List[str]) -> Tuple[int, int, int] | None:
    """
    Find the palindrome pair that results in the longest palindrome.
    
    Args:
        words: List of words to search
        
    Returns:
        Tuple[int, int, int]: (index1, index2, length) or None if none found
    """
    _validate_word_list(words)
    
    pairs = find_palindrome_pairs(words)
    
    if not pairs:
        return None
    
    longest_pair = None
    max_length = 0
    
    for i, j in pairs:
        palindrome = words[i] + words[j]
        if len(palindrome) > max_length:
            max_length = len(palindrome)
            longest_pair = (i, j, max_length)
    
    return longest_pair