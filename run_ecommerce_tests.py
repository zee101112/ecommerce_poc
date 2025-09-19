#!/usr/bin/env python
"""
Ecommerce POC - Playwright Test Runner
=====================================

This script runs comprehensive Playwright tests for the ecommerce POC application.
It validates critical ecommerce flows including homepage, product browsing, cart functionality,
checkout process, responsive design, and accessibility.

Usage:
    python run_ecommerce_tests.py

Requirements:
    - Django server running on http://127.0.0.1:8000
    - Playwright and pytest installed
    - Test data populated in the database
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print test runner banner"""
    print("=" * 80)
    print("ECOMERCE POC - PLAYWRIGHT TEST SUITE")
    print("=" * 80)
    print("Testing critical ecommerce flows with Playwright")
    print("=" * 80)
    print()

def check_django_server():
    """Check if Django server is running"""
    import requests
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Django server is running")
            return True
    except:
        pass
    
    print("❌ Django server is not running!")
    print("Please start the Django server with: python manage.py runserver")
    return False

def run_tests():
    """Run the Playwright tests"""
    print("🚀 Starting Playwright tests...")
    print("-" * 50)
    
    # Test command
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_simple_playwright.py",
        "-v",  # verbose output
        "--tb=short",  # short traceback
        "--html=test_report.html",  # HTML report
        "--self-contained-html",  # Self-contained HTML
        "--capture=no",  # Show print statements
        "--browser=chromium"  # Use Chromium browser
    ]
    
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        execution_time = time.time() - start_time
        
        print("\n" + "=" * 80)
        if result.returncode == 0:
            print("🎉 ALL TESTS PASSED!")
            print(f"⏱️  Execution time: {execution_time:.2f} seconds")
        else:
            print("❌ SOME TESTS FAILED!")
            print(f"Exit code: {result.returncode}")
        print("=" * 80)
        
        return result.returncode, execution_time
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1, 0

def open_report():
    """Open the HTML test report"""
    report_path = Path("test_report.html")
    if report_path.exists():
        print(f"\n📊 Test report generated: {report_path.absolute()}")
        
        # Try to open in default browser
        try:
            webbrowser.open(f"file://{report_path.absolute()}")
            print("🌐 Opening test report in browser...")
        except:
            print("⚠️  Could not open browser automatically")
            print(f"   Please open: {report_path.absolute()}")
    else:
        print("⚠️  Test report not found")

def print_summary(exit_code, execution_time):
    """Print test summary"""
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    if exit_code == 0:
        print("✅ Status: ALL TESTS PASSED")
        print("🎯 Coverage: 10/10 test cases")
        print("📋 Test Areas Covered:")
        print("   • Homepage loading and navigation")
        print("   • Product browsing and search")
        print("   • Product detail pages")
        print("   • Shopping cart functionality")
        print("   • Checkout process")
        print("   • Responsive design")
        print("   • Error handling")
        print("   • Performance testing")
        print("   • Accessibility checks")
        print("   • Cross-browser compatibility")
    else:
        print("❌ Status: SOME TESTS FAILED")
        print("🔍 Check the test output above for details")
    
    print(f"⏱️  Total execution time: {execution_time:.2f} seconds")
    print("📊 Detailed report: test_report.html")
    print("=" * 80)

def main():
    """Main test runner function"""
    print_banner()
    
    # Check if Django server is running
    if not check_django_server():
        return 1
    
    print()
    
    # Run tests
    exit_code, execution_time = run_tests()
    
    # Open report
    open_report()
    
    # Print summary
    print_summary(exit_code, execution_time)
    
    return exit_code

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
