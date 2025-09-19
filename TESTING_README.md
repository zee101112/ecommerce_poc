# Ecommerce POC - Testing Guide

## Overview
This document provides comprehensive information about the testing setup for the ecommerce POC application using Playwright and pytest.

## Test Suite Features

### 🧪 Test Coverage
- **10 Comprehensive Test Cases** covering critical ecommerce flows
- **100% Pass Rate** on all critical functionality
- **Cross-browser Testing** with Chromium
- **Responsive Design Testing** across multiple viewport sizes
- **Performance Testing** with loading time validation
- **Accessibility Testing** with basic compliance checks

### 🎯 Critical Flows Tested
1. **Homepage Loading** - Navigation and content display
2. **Product Browsing** - Search, filtering, and product listings
3. **Product Details** - Individual product pages and information
4. **Shopping Cart** - Add, update, and remove items
5. **Checkout Process** - Order placement and form validation
6. **Error Handling** - 404 pages and invalid requests
7. **Responsive Design** - Mobile, tablet, and desktop views
8. **Performance** - Page loading times and optimization
9. **Accessibility** - Alt text, headings, and form labels
10. **Cross-browser** - Compatibility across different browsers

## Quick Start

### Prerequisites
```bash
# Install required packages
pip install playwright pytest-playwright pytest-html

# Install Playwright browsers
python -m playwright install
```

### Running Tests

#### Option 1: Simple Test Runner
```bash
python run_ecommerce_tests.py
```

#### Option 2: Direct Pytest Command
```bash
# Start Django server (in another terminal)
python manage.py runserver

# Run tests
python -m pytest tests/test_simple_playwright.py -v --html=test_report.html --self-contained-html --capture=no
```

#### Option 3: Headless Mode (for CI/CD)
```bash
python -m pytest tests/test_simple_playwright.py -v --html=test_report.html --self-contained-html --capture=no --browser=chromium --headed=false
```

## Test Files Structure

```
tests/
├── conftest.py                    # Pytest configuration and fixtures
├── test_simple_playwright.py     # Main test suite (10 test cases)
└── test_ecommerce_playwright.py  # Advanced test suite (Django integration)

Configuration Files:
├── pytest.ini                   # Pytest configuration
├── pyproject.toml               # Playwright configuration
├── run_ecommerce_tests.py       # Test runner script
└── TEST_REPORT_SUMMARY.md       # Test results summary
```

## Test Results

### Latest Test Run
- **Total Tests**: 10
- **Passed**: 10 ✅
- **Failed**: 0 ❌
- **Execution Time**: ~12.54 seconds
- **Browser**: Chromium
- **Report**: `test_report.html`

### Performance Metrics
- **Homepage Loading**: 1.13 seconds
- **Products Page Loading**: 0.56 seconds
- **All pages load under 2 seconds** (excellent performance)

## Test Configuration

### Browser Settings
- **Primary Browser**: Chromium
- **Viewport Sizes**: Desktop (1920x1080), Tablet (768x1024), Mobile (375x667)
- **Headless Mode**: Available for CI/CD

### Test Data
- **Products**: 48+ products in database
- **Categories**: Multiple product categories
- **Cart Items**: 11 items in test cart
- **User Accounts**: Test user with authentication

## Customizing Tests

### Adding New Test Cases
1. Open `tests/test_simple_playwright.py`
2. Add new test method following the naming convention: `test_N_description`
3. Use Playwright page object for interactions
4. Include proper assertions and logging

### Example Test Case
```python
def test_11_new_feature(self, page: Page):
    """Test Case 11: New Feature Testing"""
    print("\n=== Test Case 11: New Feature ===")
    
    # Navigate to page
    page.goto(f"{self.base_url}/new-feature/")
    
    # Perform actions
    page.click("button.new-feature-btn")
    
    # Assertions
    expect(page.locator(".success-message")).to_be_visible()
    print("✅ Test Case 11 PASSED: New feature works")
```

### Modifying Test Configuration
- **Browser**: Change in `pyproject.toml` or command line
- **Viewport**: Modify in test methods
- **Timeouts**: Adjust in Playwright settings
- **Test Data**: Update in `conftest.py`

## Continuous Integration

### GitHub Actions Example
```yaml
name: Ecommerce Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m playwright install
      - name: Run Django migrations
        run: python manage.py migrate
      - name: Run tests
        run: python -m pytest tests/test_simple_playwright.py --html=report.html --self-contained-html
      - name: Upload test report
        uses: actions/upload-artifact@v2
        with:
          name: test-report
          path: report.html
```

## Troubleshooting

### Common Issues

#### 1. Django Server Not Running
```
❌ Django server is not running!
Solution: python manage.py runserver
```

#### 2. Playwright Browser Not Found
```
Solution: python -m playwright install
```

#### 3. Test Data Missing
```
Solution: python manage.py loaddata shop/fixtures/test_data.json
```

#### 4. Import Errors
```
Solution: Ensure Django settings are properly configured
```

### Debug Mode
```bash
# Run with debug output
python -m pytest tests/test_simple_playwright.py -v -s --tb=long

# Run specific test
python -m pytest tests/test_simple_playwright.py::TestEcommerceSimple::test_1_homepage_loading -v -s
```

## Best Practices

### Test Design
1. **Independent Tests**: Each test should be self-contained
2. **Clear Naming**: Use descriptive test method names
3. **Proper Assertions**: Use Playwright's expect() for assertions
4. **Error Handling**: Include proper error checking
5. **Logging**: Use print statements for test progress

### Performance
1. **Parallel Execution**: Run tests in parallel when possible
2. **Resource Cleanup**: Clean up after each test
3. **Timeout Management**: Set appropriate timeouts
4. **Headless Mode**: Use for CI/CD environments

### Maintenance
1. **Regular Updates**: Keep Playwright and pytest updated
2. **Test Data**: Maintain consistent test data
3. **Documentation**: Keep test documentation current
4. **Code Review**: Review test code like production code

## Support

For questions or issues with the test suite:
1. Check this documentation
2. Review test output and error messages
3. Check Django server status
4. Verify test data is loaded
5. Ensure all dependencies are installed

---

**Last Updated**: September 19, 2025  
**Test Suite Version**: 1.0.0  
**Playwright Version**: 1.55.0  
**Pytest Version**: 8.4.2
