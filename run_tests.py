#!/usr/bin/env python
"""
Test runner script for ecommerce Playwright tests
"""
import os
import sys
import subprocess
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_poc.settings')
django.setup()

def run_tests():
    """Run the Playwright tests with detailed reporting"""
    print("=" * 80)
    print("ECOMERCE POC - PLAYWRIGHT TEST SUITE")
    print("=" * 80)
    print()
    
    # Ensure Django server is running
    print("Starting Django development server...")
    print("Note: Make sure to run 'python manage.py runserver' in another terminal")
    print("Press Enter when the server is running...")
    input()
    
    # Run Playwright tests
    print("\nRunning Playwright tests...")
    print("-" * 50)
    
    try:
        # Run tests with detailed output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_ecommerce_playwright.py",
            "-v",  # verbose output
            "--tb=short",  # short traceback
            "--html=test_report.html",  # HTML report
            "--self-contained-html",  # Self-contained HTML
            "--capture=no",  # Show print statements
            "--browser=chromium",  # Use Chromium browser
            "--headed"  # Show browser (for debugging)
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n" + "=" * 80)
            print("✅ ALL TESTS PASSED!")
            print("=" * 80)
            print("\nTest Report: test_report.html")
        else:
            print("\n" + "=" * 80)
            print("❌ SOME TESTS FAILED!")
            print("=" * 80)
            print(f"Exit code: {result.returncode}")
        
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
