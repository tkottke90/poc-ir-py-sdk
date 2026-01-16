# Server Context Implementation

This document explains the context-based dependency injection pattern used in the HTTP server.

## Overview

The server uses a **Context Object** pattern to provide dependencies (telemetry handler, state, and logger) to HTTP endpoint handlers without relying on global variables.

## Architecture

### ServerContext Class

Located in `src/server/context.py`, this class holds all dependencies needed by endpoint handlers:

```python
class ServerContext:
    def __init__(self, get_ir: Callable, get_state: Callable, logger: Logger):
        self.get_ir = get_ir      # Getter for TelemetryHandler
        self.get_state = get_state # Getter for State
        self.logger = logger       # Logger instance
    
    @property
    def ir(self):
        """Get the current TelemetryHandler instance"""
        return self.get_ir()
    
    @property
    def state(self):
        """Get the current State instance"""
        return self.get_state()
```

### Benefits

1. **No Global Variables** - Dependencies are passed explicitly through the context
2. **Lazy Evaluation** - Values are fetched on-demand using getters
3. **Testable** - Easy to mock the entire context for testing
4. **Clean API** - Handlers receive a single `ctx` parameter instead of multiple arguments
5. **Logger Access** - All handlers can log using `ctx.logger`

## Usage

### In main.py

```python
from server import ServerContext, start_server, handle_root, handle_driver, handle_camera

# Create API logger
api_logger = setup_logger('iracing.api', console_output=False)

# Create context with getters
context = ServerContext(
    get_ir=lambda: ir,      # Captures ir from closure
    get_state=lambda: state, # Captures state from closure
    logger=api_logger
)

# Start server with context
http_server = start_server(
    endpoints={
        '/': handle_root,
        '/api/driver': handle_driver,
        '/api/camera': handle_camera
    },
    context=context,
    port=9000
)
```

### In Endpoint Handlers

```python
def handle_driver(handler, ctx: ServerContext):
    """Handle driver data endpoint"""
    try:
        # Get current values using context properties
        ir = ctx.ir
        state = ctx.state
        
        # Log using context logger
        ctx.logger.debug('Driver endpoint called')
        
        if not state.ir_connected:
            ctx.logger.warning('Not connected to iRacing')
            send_error_response(handler, 'Not connected to iRacing', 503)
            return
        
        # ... rest of handler logic
        
        ctx.logger.info(f'Driver data returned: {driver.UserName}')
        send_json_response(handler, response)
        
    except Exception as e:
        ctx.logger.error(f'Error in driver endpoint: {e}')
        send_error_response(handler, str(e))
```

## File Structure

```
src/server/
├── __init__.py       # Exports ServerContext, start_server, and handlers
├── context.py        # ServerContext class definition
├── server.py         # HTTP server implementation
├── helpers.py        # JSON response helpers
├── root.py           # Root endpoint handler
├── driver.py         # Driver data endpoint handler
└── camera.py         # Camera info endpoint handler
```

## Comparison to JavaScript

This pattern is similar to dependency injection in JavaScript frameworks:

**JavaScript (Express/NestJS style):**
```typescript
const context = {
  getIr: () => ir,
  getState: () => state,
  logger: logger
};

app.get('/api/driver', (req, res) => {
  const ir = context.getIr();
  const state = context.getState();
  context.logger.info('Driver endpoint called');
  // ...
});
```

**Python (Our implementation):**
```python
context = ServerContext(
    get_ir=lambda: ir,
    get_state=lambda: state,
    logger=logger
)

def handle_driver(handler, ctx):
    ir = ctx.ir
    state = ctx.state
    ctx.logger.info('Driver endpoint called')
    # ...
```

## Adding New Endpoints

To add a new endpoint:

1. Create a handler function in `src/server/your_endpoint.py`:
   ```python
   from .helpers import send_json_response
   from .context import ServerContext
   
   def handle_your_endpoint(handler, ctx: ServerContext):
       ctx.logger.debug('Your endpoint called')
       # Your logic here
       send_json_response(handler, {'data': 'value'})
   ```

2. Export it in `src/server/__init__.py`:
   ```python
   from server.your_endpoint import handle_your_endpoint
   __all__ = [..., 'handle_your_endpoint']
   ```

3. Register it in `main.py`:
   ```python
   http_server = start_server(
       endpoints={
           # ... existing endpoints
           '/api/your-endpoint': handle_your_endpoint
       },
       context=context,
       port=9000
   )
   ```

## Testing

The context pattern makes testing easy:

```python
from server.context import ServerContext
from server.driver import handle_driver
from unittest.mock import Mock

# Create mock context
mock_logger = Mock()
mock_ir = Mock()
mock_state = Mock()

context = ServerContext(
    get_ir=lambda: mock_ir,
    get_state=lambda: mock_state,
    logger=mock_logger
)

# Test handler
handle_driver(mock_handler, context)

# Verify logger was called
mock_logger.debug.assert_called_with('Driver endpoint called')
```

