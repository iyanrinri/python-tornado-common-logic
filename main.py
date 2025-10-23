"""
Main Tornado application module.

This module contains the main Tornado application setup, configuration,
and startup logic for the median calculation service.
"""

import logging
import logging.handlers
import os
import signal
import sys
from pathlib import Path

import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line

from app.routes import get_url_patterns
from config.settings import get_config

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Define command line options
define("port", default=8888, help="Port to listen on", type=int)
define("debug", default=False, help="Enable debug mode", type=bool)
define("config-file", default=None, help="Path to config file", type=str)

# Configure logging
logger = logging.getLogger(__name__)


def setup_logging(config):
    """
    Set up application logging.
    
    Args:
        config: Configuration object containing logging settings
    """
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # Create logs directory if it doesn't exist
    log_dir = Path(config.LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)
    except (OSError, IOError) as e:
        logger.warning(f"Could not set up file logging: {e}")
    
    logger.info(f"Logging configured with level: {config.LOG_LEVEL}")


def create_application(config):
    """
    Create and configure the Tornado application.
    
    Args:
        config: Configuration object
        
    Returns:
        tornado.web.Application: Configured Tornado application
    """
    # Application settings
    settings = {
        "debug": config.DEBUG,
        "autoreload": config.DEBUG,
        "serve_traceback": config.DEBUG,
        "compress_response": True,
        "default_handler_class": NotFoundHandler,
        "default_handler_args": {"status_code": 404},
    }
    
    # Get URL patterns
    url_patterns = get_url_patterns()
    
    # Create application
    app = tornado.web.Application(url_patterns, **settings)
    
    # Store config in application for access by handlers
    app.config = config
    
    logger.info(f"Tornado application created with {len(url_patterns)} routes")
    
    return app


class NotFoundHandler(tornado.web.RequestHandler):
    """Custom 404 handler that returns JSON."""
    
    def initialize(self, status_code):
        """Initialize with status code."""
        self.set_status(status_code)
    
    def set_default_headers(self):
        """Set default headers."""
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
    
    def prepare(self):
        """Handle all HTTP methods."""
        if self.request.method != "OPTIONS":
            self.write({
                "error": "Not Found",
                "error_code": "NOT_FOUND",
                "message": f"The requested URL {self.request.uri} was not found on this server.",
                "timestamp": tornado.web.datetime.datetime.utcnow().isoformat() + "Z"
            })


def setup_signal_handlers():
    """Set up signal handlers for graceful shutdown."""
    
    def signal_handler(signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        
        # Stop the IOLoop
        ioloop = tornado.ioloop.IOLoop.current()
        ioloop.add_callback_from_signal(shutdown)
    
    def shutdown():
        """Perform graceful shutdown."""
        logger.info("Shutting down application...")
        
        # Add any cleanup logic here
        # For example: close database connections, save state, etc.
        
        # Stop the IOLoop
        tornado.ioloop.IOLoop.current().stop()
        logger.info("Application shutdown complete")
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info("Signal handlers registered")


def validate_environment():
    """Validate that the environment is properly set up."""
    try:
        # Test imports to ensure all dependencies are available
        from app.utils.array_operations import find_median_sorted_arrays
        from app.services import median_service, health_service
        
        # Test basic functionality
        test_result = find_median_sorted_arrays([1, 2], [3, 4])
        if test_result != 2.5:
            raise RuntimeError("Basic functionality test failed")
        
        logger.info("Environment validation passed")
        return True
        
    except Exception as e:
        logger.error(f"Environment validation failed: {e}")
        return False


def main():
    """Main application entry point."""
    # Parse command line arguments
    parse_command_line()
    
    # Load configuration
    config = get_config()
    
    # Override config with command line options if provided
    if options.port:
        config.PORT = options.port
    if options.debug is not None:
        config.DEBUG = options.debug
    
    # Set up logging
    setup_logging(config)
    
    logger.info("=" * 50)
    logger.info("Starting Tornado Median Calculator Service")
    logger.info("=" * 50)
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Debug mode: {config.DEBUG}")
    logger.info(f"Port: {config.PORT}")
    logger.info(f"Host: {config.HOST}")
    
    # Validate environment
    if not validate_environment():
        logger.error("Environment validation failed, exiting")
        sys.exit(1)
    
    # Create application
    try:
        app = create_application(config)
    except Exception as e:
        logger.error(f"Failed to create application: {e}")
        sys.exit(1)
    
    # Set up signal handlers
    setup_signal_handlers()
    
    # Start the server
    try:
        app.listen(config.PORT, config.HOST)
        logger.info(f"Server started on http://{config.HOST}:{config.PORT}")
        logger.info("Available endpoints:")
        logger.info("  POST /api/v1/median - Calculate median of two arrays")
        logger.info("  POST /api/v1/median/batch - Batch median calculations")
        logger.info("  GET  /api/v1/median/stats - Get service statistics")
        logger.info("  DELETE /api/v1/median/stats - Reset service statistics")
        logger.info("  GET  /health - Health check")
        logger.info("  GET  /status - Detailed status")
        logger.info("  GET  /ready - Readiness probe")
        logger.info("  GET  /live - Liveness probe")
        logger.info("=" * 50)
        
        # Start the IOLoop
        tornado.ioloop.IOLoop.current().start()
        
    except OSError as e:
        logger.error(f"Failed to start server: {e}")
        if e.errno == 48:  # Address already in use
            logger.error(f"Port {config.PORT} is already in use")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        logger.info("Server stopped")


if __name__ == "__main__":
    main()