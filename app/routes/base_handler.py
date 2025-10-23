"""
Base handler class with common functionality.

This module provides a base handler class that includes common
functionality like CORS handling, error handling, and JSON utilities.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

import tornado.web
from tornado.web import HTTPError

logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
    """Base handler class with common functionality."""
    
    def set_default_headers(self):
        """Set default headers for all responses."""
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    
    def options(self, *args):
        """Handle OPTIONS requests for CORS."""
        self.set_status(204)
        self.finish()
    
    def write_json(self, data: Dict[str, Any], status_code: int = 200) -> None:
        """
        Write JSON response with proper status code.
        
        Args:
            data: Dictionary to serialize as JSON
            status_code: HTTP status code (default: 200)
        """
        self.set_status(status_code)
        self.write(json.dumps(data, indent=2))
    
    def write_error_json(self, error_message: str, error_code: str = "INTERNAL_ERROR", 
                        status_code: int = 500, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Write error response in JSON format.
        
        Args:
            error_message: Human-readable error message
            error_code: Machine-readable error code
            status_code: HTTP status code
            details: Optional additional error details
        """
        error_response = {
            "error": error_message,
            "error_code": error_code,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        if details:
            error_response["details"] = details
        
        self.write_json(error_response, status_code)
    
    def get_json_body(self) -> Dict[str, Any]:
        """
        Parse and validate JSON request body.
        
        Returns:
            Dict: Parsed JSON data
            
        Raises:
            HTTPError: If JSON parsing fails
        """
        try:
            if not self.request.body:
                raise HTTPError(400, "Request body is empty")
            
            body = json.loads(self.request.body.decode('utf-8'))
            
            if not isinstance(body, dict):
                raise HTTPError(400, "Request body must be a JSON object")
            
            return body
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise HTTPError(400, f"Invalid JSON: {str(e)}")
        except UnicodeDecodeError as e:
            logger.error(f"Unicode decode error: {e}")
            raise HTTPError(400, f"Invalid encoding: {str(e)}")
    
    def write_error(self, status_code: int, **kwargs) -> None:
        """
        Override default error handler to return JSON.
        
        Args:
            status_code: HTTP status code
            **kwargs: Additional arguments (including 'reason' and 'exc_info')
        """
        reason = kwargs.get('reason', self._reason)
        exc_info = kwargs.get('exc_info')
        
        # Log the error
        if exc_info:
            logger.error(f"Handler error {status_code}: {reason}", exc_info=exc_info[1])
        else:
            logger.error(f"Handler error {status_code}: {reason}")
        
        # Determine error code based on status
        error_codes = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED", 
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
            422: "VALIDATION_ERROR",
            500: "INTERNAL_ERROR",
            503: "SERVICE_UNAVAILABLE"
        }
        
        error_code = error_codes.get(status_code, "UNKNOWN_ERROR")
        
        # Don't include sensitive error details in production
        if self.settings.get("debug", False) and exc_info:
            details = {
                "exception_type": exc_info[0].__name__ if exc_info[0] else None,
                "exception_message": str(exc_info[1]) if exc_info[1] else None
            }
        else:
            details = None
        
        self.write_error_json(
            error_message=reason or "An error occurred",
            error_code=error_code,
            status_code=status_code,
            details=details
        )
    
    async def prepare(self):
        """Called before each request method."""
        # Log request information
        logger.info(f"{self.request.method} {self.request.uri} from {self.request.remote_ip}")
        
        # Add request start time for performance monitoring
        self.request_start_time = datetime.utcnow()
    
    def on_finish(self):
        """Called after the request is finished."""
        if hasattr(self, 'request_start_time'):
            duration = (datetime.utcnow() - self.request_start_time).total_seconds() * 1000
            logger.info(f"Request completed in {duration:.2f}ms with status {self.get_status()}")
    
    def get_current_user(self):
        """
        Get current user (placeholder for authentication).
        
        Override this method to implement authentication logic.
        """
        return None