#!/usr/bin/env python3
"""
Quick verification script to test the ServerContext implementation.
This doesn't require iRacing to be running.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from server import ServerContext
from logger import setup_logger
from unittest.mock import Mock

def test_context_creation():
    """Test that we can create a ServerContext"""
    print("Testing ServerContext creation...")
    
    # Create mock dependencies
    mock_ir = Mock()
    mock_state = Mock()
    logger = setup_logger('test', console_output=True)
    
    # Create context
    context = ServerContext(
        get_ir=lambda: mock_ir,
        get_state=lambda: mock_state,
        logger=logger
    )
    
    # Test that we can access properties
    assert context.ir == mock_ir, "Failed to get ir from context"
    assert context.state == mock_state, "Failed to get state from context"
    assert context.logger == logger, "Failed to get logger from context"
    
    print("✓ ServerContext creation successful")
    return True

def test_handler_imports():
    """Test that we can import all handlers"""
    print("\nTesting handler imports...")
    
    try:
        from server import handle_root, handle_driver, handle_camera
        print("✓ All handlers imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import handlers: {e}")
        return False

def test_handler_signature():
    """Test that handlers have the correct signature"""
    print("\nTesting handler signatures...")
    
    from server import handle_driver, ServerContext
    from unittest.mock import Mock
    import inspect
    
    # Check signature
    sig = inspect.signature(handle_driver)
    params = list(sig.parameters.keys())
    
    assert len(params) == 2, f"Expected 2 parameters, got {len(params)}"
    assert params[0] == 'handler', f"First param should be 'handler', got '{params[0]}'"
    assert params[1] == 'ctx', f"Second param should be 'ctx', got '{params[1]}'"
    
    # Check type hint
    ctx_param = sig.parameters['ctx']
    assert ctx_param.annotation == ServerContext, "ctx parameter should be typed as ServerContext"
    
    print("✓ Handler signatures are correct")
    return True

def test_logger_in_context():
    """Test that logger is accessible in context"""
    print("\nTesting logger accessibility...")
    
    from server import ServerContext
    from logger import setup_logger
    from unittest.mock import Mock
    
    logger = setup_logger('test.api', console_output=False)
    
    context = ServerContext(
        get_ir=lambda: Mock(),
        get_state=lambda: Mock(),
        logger=logger
    )
    
    # Test logging
    context.logger.info("Test log message")
    context.logger.debug("Debug message")
    context.logger.warning("Warning message")
    
    print("✓ Logger is accessible and working")
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("ServerContext Implementation Verification")
    print("=" * 60)
    
    tests = [
        test_context_creation,
        test_handler_imports,
        test_handler_signature,
        test_logger_in_context
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✓ All tests passed ({passed}/{total})")
        print("=" * 60)
        print("\nThe ServerContext implementation is working correctly!")
        print("\nYou can now:")
        print("  1. Start the server with: python src/main.py")
        print("  2. Test endpoints at: http://localhost:9000/api/driver")
        print("  3. Check logs for API activity in the log files")
        return 0
    else:
        print(f"✗ Some tests failed ({passed}/{total} passed)")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())

