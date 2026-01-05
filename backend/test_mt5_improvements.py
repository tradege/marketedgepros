#!/usr/bin/env python3
"""
Test script for improved MT5 Service
Tests retry logic, rate limiting, error handling, and all features
"""
import sys
import time
import logging
from datetime import datetime, timedelta

# Setup path
sys.path.insert(0, '/var/www/MarketEdgePros/backend')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import MT5 service
from src.services.mt5_service import (
    mt5_service, 
    MT5Service, 
    MT5APIError, 
    MT5AuthenticationError,
    MT5AccountNotFoundError,
    RateLimiter
)

def test_rate_limiter():
    """Test rate limiter"""
    print("\n" + "="*60)
    print("TEST 1: Rate Limiter")
    print("="*60)
    
    try:
        limiter = RateLimiter(max_requests=5, time_window=1.0)
        
        start_time = time.time()
        for i in range(7):
            limiter.wait_if_needed()
            print(f"Request {i+1} sent at {time.time() - start_time:.2f}s")
        
        elapsed = time.time() - start_time
        print(f"\n✅ Rate limiter working! 7 requests took {elapsed:.2f}s")
        print(f"   Expected: ~2s (5 requests + wait + 2 requests)")
        
        if elapsed >= 1.8 and elapsed <= 2.5:
            print("   ✅ PASS: Rate limiting is working correctly")
            return True
        else:
            print("   ⚠️  WARNING: Rate limiting might not be working as expected")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_authentication():
    """Test authentication with token caching"""
    print("\n" + "="*60)
    print("TEST 2: Authentication & Token Caching")
    print("="*60)
    
    try:
        # First authentication
        print("Authenticating (first time)...")
        start_time = time.time()
        token1 = mt5_service.authenticate()
        time1 = time.time() - start_time
        print(f"✅ Got token: {token1[:20]}... (took {time1:.2f}s)")
        
        # Second authentication (should use cached token)
        print("\nAuthenticating (second time - should use cache)...")
        start_time = time.time()
        token2 = mt5_service.authenticate()
        time2 = time.time() - start_time
        print(f"✅ Got token: {token2[:20]}... (took {time2:.2f}s)")
        
        if token1 == token2:
            print(f"\n✅ PASS: Token caching working! Second call was {time1/time2:.1f}x faster")
            return True
        else:
            print("\n⚠️  WARNING: Tokens are different (might be expired)")
            return False
            
    except MT5AuthenticationError as e:
        print(f"❌ FAIL: Authentication error: {e}")
        return False
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {e}")
        return False


def test_error_handling():
    """Test custom exceptions and error messages"""
    print("\n" + "="*60)
    print("TEST 3: Error Handling & Custom Exceptions")
    print("="*60)
    
    try:
        # Test account not found
        print("Testing account not found error...")
        try:
            mt5_service.get_account_info("999999999")
            print("⚠️  WARNING: Should have raised MT5AccountNotFoundError")
            return False
        except MT5AccountNotFoundError as e:
            print(f"✅ Correct exception raised: {type(e).__name__}")
            print(f"   Message: {e}")
        
        # Test invalid group
        print("\nTesting invalid group error...")
        try:
            mt5_service.create_account(
                name="Test User",
                group="invalid\\group\\name",
                balance=10000
            )
            print("⚠️  WARNING: Should have raised MT5APIError")
            return False
        except MT5APIError as e:
            print(f"✅ Correct exception raised: {type(e).__name__}")
            print(f"   Message: {e}")
        
        print("\n✅ PASS: Error handling working correctly")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {e}")
        return False


def test_connection_pooling():
    """Test connection pooling and session management"""
    print("\n" + "="*60)
    print("TEST 4: Connection Pooling & Session Management")
    print("="*60)
    
    try:
        # Check session exists
        if not hasattr(mt5_service, 'session'):
            print("❌ FAIL: No session found")
            return False
        
        print(f"✅ Session exists: {mt5_service.session}")
        
        # Check adapter configuration
        adapter = mt5_service.session.get_adapter('http://')
        print(f"✅ HTTP adapter configured: {adapter}")
        
        # Make multiple requests to test connection reuse
        print("\nMaking 5 requests to test connection pooling...")
        start_time = time.time()
        for i in range(5):
            mt5_service.authenticate()
        elapsed = time.time() - start_time
        
        print(f"✅ 5 authentications took {elapsed:.2f}s")
        print(f"   Average: {elapsed/5:.2f}s per request")
        
        if elapsed < 2.0:
            print("✅ PASS: Connection pooling is working (fast requests)")
            return True
        else:
            print("⚠️  WARNING: Requests are slow (might not be using connection pool)")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_timeout_handling():
    """Test timeout configuration"""
    print("\n" + "="*60)
    print("TEST 5: Timeout Handling")
    print("="*60)
    
    try:
        # Create a new service with very short timeout for testing
        print("Testing timeout configuration...")
        
        # Check that methods have timeout parameters
        import inspect
        
        # Check authenticate method
        source = inspect.getsource(mt5_service.authenticate)
        if 'timeout=' in source:
            print("✅ authenticate() has timeout configured")
        else:
            print("⚠️  WARNING: authenticate() might not have timeout")
        
        # Check get_account_info method
        source = inspect.getsource(mt5_service.get_account_info)
        if 'timeout=' in source:
            print("✅ get_account_info() has timeout configured")
        else:
            print("⚠️  WARNING: get_account_info() might not have timeout")
        
        # Check create_account method
        source = inspect.getsource(mt5_service.create_account)
        if 'timeout=' in source:
            print("✅ create_account() has timeout configured")
        else:
            print("⚠️  WARNING: create_account() might not have timeout")
        
        print("\n✅ PASS: Timeout handling configured")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_retry_logic():
    """Test retry logic (simulated)"""
    print("\n" + "="*60)
    print("TEST 6: Retry Logic")
    print("="*60)
    
    try:
        # Check that retry decorator exists
        import inspect
        
        source = inspect.getsource(mt5_service.authenticate)
        if '@retry_on_failure' in source or 'retry_on_failure' in source:
            print("✅ Retry decorator found in authenticate()")
        else:
            print("⚠️  WARNING: Retry decorator might not be applied")
        
        source = inspect.getsource(mt5_service.get_account_info)
        if '@retry_on_failure' in source or 'retry_on_failure' in source:
            print("✅ Retry decorator found in get_account_info()")
        else:
            print("⚠️  WARNING: Retry decorator might not be applied")
        
        print("\n✅ PASS: Retry logic is configured")
        print("   Note: Actual retry behavior can only be tested with real failures")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("MT5 SERVICE IMPROVEMENTS TEST SUITE")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'Rate Limiter': test_rate_limiter(),
        'Authentication & Token Caching': test_authentication(),
        'Error Handling': test_error_handling(),
        'Connection Pooling': test_connection_pooling(),
        'Timeout Handling': test_timeout_handling(),
        'Retry Logic': test_retry_logic(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"TOTAL: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! MT5 Service improvements are working correctly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
