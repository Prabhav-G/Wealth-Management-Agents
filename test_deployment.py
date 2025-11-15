#!/usr/bin/env python3
"""
Quick test to verify the deployment is working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_web_ui():
    """Test that the web UI loads"""
    print("Testing Web UI...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200 and "Financial Advisory System" in response.text:
            print("✓ Web UI is accessible")
            return True
        else:
            print(f"✗ Web UI returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Web UI error: {e}")
        return False

def test_static_files():
    """Test that static files are served"""
    print("\nTesting Static Files...")
    try:
        response = requests.get(f"{BASE_URL}/static/styles.css")
        if response.status_code == 200:
            print("✓ CSS file is accessible")
            return True
        else:
            print(f"✗ CSS file returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Static files error: {e}")
        return False

def test_api_endpoint():
    """Test that the API endpoint exists and validates input"""
    print("\nTesting API Endpoint...")
    try:
        # Test with invalid data (should return validation error, not server error)
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json={"test": "invalid"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 422:  # Validation error is expected
            print("✓ API endpoint is accessible and validating input")
            return True
        else:
            print(f"✗ API returned unexpected status {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"✗ API endpoint error: {e}")
        return False

def main():
    print("=" * 50)
    print("DEPLOYMENT TEST")
    print("=" * 50)
    
    results = []
    results.append(test_web_ui())
    results.append(test_static_files())
    results.append(test_api_endpoint())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ ALL TESTS PASSED - Deployment is working!")
        print(f"\n🌐 Open your browser to: {BASE_URL}")
    else:
        print("⚠️  SOME TESTS FAILED - Check the errors above")
    print("=" * 50)

if __name__ == "__main__":
    main()

