"""
Server context for dependency injection.

This module provides a context object that holds all dependencies needed by
HTTP endpoint handlers, enabling clean dependency injection without globals.
"""

from typing import Callable
from logging import Logger


class ServerContext:
    """
    Context object that holds dependencies for HTTP endpoint handlers.
    
    This allows handlers to access telemetry data and logging without
    relying on global variables.
    """
    
    def __init__(
        self,
        get_ir: Callable,
        get_state: Callable,
        logger: Logger
    ):
        """
        Initialize the server context.
        
        Args:
            get_ir: Callable that returns the current TelemetryHandler instance
            get_state: Callable that returns the current State instance
            logger: Logger instance for HTTP handlers
        """
        self.get_ir = get_ir
        self.get_state = get_state
        self.logger = logger
    
    @property
    def ir(self):
        """Get the current TelemetryHandler instance"""
        return self.get_ir()
    
    @property
    def state(self):
        """Get the current State instance"""
        return self.get_state()

