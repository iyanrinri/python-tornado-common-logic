"""
Routes package for Tornado handlers.

This package contains all the request handlers and routing configuration
for the Tornado web application.
"""

from .base_handler import BaseHandler
from .median_handlers_simple import MedianHandler, MedianStatsHandler, MedianBatchHandler
from .health_handlers import HealthHandler, StatusHandler, ReadinessHandler, LivenessHandler

__all__ = [
    'BaseHandler',
    'MedianHandler', 
    'MedianStatsHandler', 
    'MedianBatchHandler',
    'HealthHandler', 
    'StatusHandler', 
    'ReadinessHandler', 
    'LivenessHandler'
]

# URL patterns for the application
def get_url_patterns():
    """
    Get URL patterns for the Tornado application.
    
    Returns:
        List of URL patterns for routing
    """
    return [
        # Median calculation endpoints
        (r"/api/v1/median", MedianHandler),
        (r"/api/v1/median/batch", MedianBatchHandler),
        (r"/api/v1/median/stats", MedianStatsHandler),
        
        # Health and monitoring endpoints
        (r"/health", HealthHandler),
        (r"/status", StatusHandler),
        (r"/ready", ReadinessHandler),
        (r"/live", LivenessHandler),
        
        # Alternative health endpoints (common patterns)
        (r"/health/live", LivenessHandler),
        (r"/health/ready", ReadinessHandler),
        (r"/healthz", HealthHandler),
        (r"/readyz", ReadinessHandler),
        (r"/livez", LivenessHandler),
    ]