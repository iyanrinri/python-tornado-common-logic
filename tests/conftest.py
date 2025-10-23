"""
Test configuration and fixtures.

This module contains pytest configuration and shared fixtures
for the test suite.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging for tests
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@pytest.fixture
def sample_sorted_arrays():
    """Fixture providing sample sorted arrays for testing."""
    return {
        'small_even': ([1, 3], [2, 4]),
        'small_odd': ([1, 3, 5], [2, 4, 6]),
        'empty_first': ([], [1, 2, 3]),
        'empty_second': ([1, 2, 3], []),
        'single_elements': ([1], [2]),
        'duplicates': ([1, 1, 2], [1, 2, 3]),
        'negative': ([-3, -1, 0], [-2, 1, 2]),
        'floats': ([1.1, 2.2, 3.3], [1.5, 2.5, 3.5])
    }

@pytest.fixture
def invalid_arrays():
    """Fixture providing invalid arrays for error testing."""
    return {
        'unsorted': ([3, 1, 2], [4, 5, 6]),
        'mixed_types': ([1, "2"], [3, 4]),
        'with_none': ([1, None], [3, 4]),
        'with_nan': ([1, float('nan')], [3, 4])
    }

@pytest.fixture
def expected_medians():
    """Fixture providing expected median results."""
    return {
        'small_even': 2.5,
        'small_odd': 3.5,
        'empty_first': 2.0,
        'empty_second': 2.0,
        'single_elements': 1.5,
        'duplicates': 1.5,
        'negative': -1.0,
        'floats': 2.35
    }

# Test markers
pytest_plugins = []

# Add custom markers
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "api: mark test as API test")

# Collection hook to organize test output
def pytest_collection_modifyitems(config, items):
    """Modify test items during collection."""
    for item in items:
        # Add markers based on test location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add markers based on test names
        if "test_api" in item.name or "API" in item.name:
            item.add_marker(pytest.mark.api)
        
        # Mark slow tests
        if "performance" in item.name or "large" in item.name:
            item.add_marker(pytest.mark.slow)