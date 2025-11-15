#!/usr/bin/env python3
"""
Simple test script to verify the server can start and serve files
"""
import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import fastapi
        print("✓ FastAPI imported")
    except ImportError as e:
        print(f"✗ FastAPI not found: {e}")
        print("  Run: pip install fastapi uvicorn")
        return False
    
    try:
        import api
        print("✓ API module imported")
    except Exception as e:
        print(f"✗ API module error: {e}")
        return False
    
    return True

def test_static_files():
    """Test if static files exist"""
    print("\nTesting static files...")
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    
    if not os.path.exists(static_dir):
        print(f"✗ Static directory not found: {static_dir}")
        return False
    print(f"✓ Static directory exists: {static_dir}")
    
    required_files = ["index.html", "styles.css", "script.js"]
    for file in required_files:
        file_path = os.path.join(static_dir, file)
        if os.path.exists(file_path):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} not found")
            return False
    
    return True

def main():
    print("=" * 50)
    print("Financial Advisory System - Server Test")
    print("=" * 50)
    
    imports_ok = test_imports()
    files_ok = test_static_files()
    
    print("\n" + "=" * 50)
    if imports_ok and files_ok:
        print("✓ All tests passed!")
        print("\nTo start the server, run:")
        print("  uvicorn api:app --reload --host 0.0.0.0 --port 8000")
        print("\nOr use the startup script:")
        print("  ./start_server.sh")
        return 0
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

