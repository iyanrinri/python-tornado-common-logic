"""
Health check and system status handlers.

This module contains handlers for health checks, system status,
and service monitoring endpoints.
"""

import logging
from datetime import datetime

from .base_handler import BaseHandler
from ..services import health_service

logger = logging.getLogger(__name__)


class HealthHandler(BaseHandler):
    """Handler for basic health checks."""
    
    async def get(self):
        """
        Get basic health status.
        
        Response:
        {
            "status": "healthy",
            "timestamp": "2025-10-23T10:30:00Z",
            "version": "1.0.0",
            "uptime_seconds": 3600.5
        }
        """
        try:
            health_status = await health_service.get_health_status()
            self.write_json(health_status, 200)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}", exc_info=True)
            self.write_error_json(
                error_message="Health check failed",
                error_code="HEALTH_CHECK_ERROR",
                status_code=503
            )


class StatusHandler(BaseHandler):
    """Handler for detailed system status."""
    
    async def get(self):
        """
        Get detailed system status including dependencies.
        
        Response:
        {
            "status": "healthy",
            "timestamp": "2025-10-23T10:30:00Z",
            "version": "1.0.0",
            "uptime_seconds": 3600.5,
            "dependencies": {
                "array_operations_util": "available",
                "logging_system": "active",
                "configuration": "loaded"
            },
            "service_stats": {
                "total_calls": 42,
                "total_execution_time_ms": 125.5,
                "average_execution_time_ms": 2.99,
                "service_status": "active"
            }
        }
        """
        try:
            # Get basic health status
            health_status = await health_service.get_health_status()
            
            # Get dependency status
            dependencies = health_service.check_dependencies()
            
            # Get service statistics
            from ..services import median_service
            service_stats = median_service.get_statistics()
            
            # Combine all status information
            status_response = {
                **health_status,
                "dependencies": dependencies,
                "service_stats": service_stats
            }
            
            self.write_json(status_response, 200)
            
        except Exception as e:
            logger.error(f"Status check failed: {e}", exc_info=True)
            self.write_error_json(
                error_message="Status check failed",
                error_code="STATUS_CHECK_ERROR", 
                status_code=503
            )


class ReadinessHandler(BaseHandler):
    """Handler for readiness probe (Kubernetes-style)."""
    
    async def get(self):
        """
        Check if the service is ready to accept requests.
        
        Returns 200 if ready, 503 if not ready.
        """
        try:
            # Check if all critical components are working
            dependencies = health_service.check_dependencies()
            
            # All dependencies should be available/active
            all_ready = all(
                status in ["available", "active", "loaded"] 
                for status in dependencies.values()
            )
            
            if all_ready:
                self.write_json({"status": "ready"}, 200)
            else:
                self.write_json({
                    "status": "not_ready",
                    "dependencies": dependencies
                }, 503)
                
        except Exception as e:
            logger.error(f"Readiness check failed: {e}", exc_info=True)
            self.write_json({"status": "not_ready", "error": str(e)}, 503)


class LivenessHandler(BaseHandler):
    """Handler for liveness probe (Kubernetes-style)."""
    
    async def get(self):
        """
        Check if the service is alive (basic functionality test).
        
        Returns 200 if alive, 503 if not alive.
        """
        try:
            # Simple test to ensure basic functionality
            from ..utils.array_operations import find_median_sorted_arrays
            
            # Test with simple arrays
            result = find_median_sorted_arrays([1, 2], [3, 4])
            
            if result == 2.5:  # Expected result
                self.write_json({"status": "alive"}, 200)
            else:
                self.write_json({
                    "status": "not_alive", 
                    "error": "Basic functionality test failed"
                }, 503)
                
        except Exception as e:
            logger.error(f"Liveness check failed: {e}", exc_info=True)
            self.write_json({"status": "not_alive", "error": str(e)}, 503)