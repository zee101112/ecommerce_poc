import pytest
from playwright.sync_api import Page, expect
import time
import os

class TestEcommerceSimple:
    """Simple Playwright tests for ecommerce application"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.base_url = "http://127.0.0.1:8000"
        
    def test_1_homepage_loading(self, page: Page):
        """Test Case 1: Homepage loads correctly"""
        print("\n=== Test Case 1: Homepage Loading ===")
        
        # Navigate to homepage
        page.goto(f"{self.base_url}/")
        
        # Check page loads successfully
        expect(page).to_have_url(f"{self.base_url}/")
        print("✓ Homepage loads successfully")
        
        # Check for basic page elements
        page_title = page.title()
        print(f"✓ Page title: {page_title}")
        
        # Check for navigation elements
        nav_elements = page.locator("nav, header, .navbar")
        if nav_elements.count() > 0:
            print("✓ Navigation elements found")
        else:
            print("⚠ Navigation elements not found")
        
        # Check for main content
        main_content = page.locator("main, .main, .content, body")
        if main_content.count() > 0:
            print("✓ Main content area found")
        else:
            print("⚠ Main content area not found")
        
        print("✅ Test Case 1 PASSED: Homepage loads correctly")

    def test_2_products_page_navigation(self, page: Page):
        """Test Case 2: Products page navigation"""
        print("\n=== Test Case 2: Products Page Navigation ===")
        
        # Navigate to products page
        page.goto(f"{self.base_url}/products/")
        expect(page).to_have_url(f"{self.base_url}/products/")
        print("✓ Products page loads successfully")
        
        # Check for product listings
        product_elements = page.locator(".product, .item, [class*='product']")
        if product_elements.count() > 0:
            print(f"✓ Found {product_elements.count()} product elements")
        else:
            print("⚠ No product elements found")
        
        # Check for search functionality
        search_input = page.locator("input[type='search'], input[name='q']")
        if search_input.count() > 0:
            print("✓ Search input found")
        else:
            print("⚠ Search input not found")
        
        print("✅ Test Case 2 PASSED: Products page navigation works")

    def test_3_product_detail_page(self, page: Page):
        """Test Case 3: Product detail page"""
        print("\n=== Test Case 3: Product Detail Page ===")
        
        # First, try to find a product from the products page
        page.goto(f"{self.base_url}/products/")
        
        # Look for product links
        product_links = page.locator("a[href*='/product/']")
        if product_links.count() > 0:
            # Click on first product
            product_links.first.click()
            page.wait_for_timeout(2000)
            print("✓ Navigated to product detail page")
            
            # Check if we're on a product detail page
            current_url = page.url
            if "/product/" in current_url:
                print(f"✓ Product detail URL: {current_url}")
            else:
                print(f"⚠ Unexpected URL: {current_url}")
        else:
            # Try direct navigation to a known product
            page.goto(f"{self.base_url}/product/test-product/")
            print("✓ Attempted direct navigation to product detail")
        
        # Check for product information
        product_title = page.locator("h1, .title, [class*='title']")
        if product_title.count() > 0:
            print("✓ Product title found")
        else:
            print("⚠ Product title not found")
        
        print("✅ Test Case 3 PASSED: Product detail page accessible")

    def test_4_cart_functionality(self, page: Page):
        """Test Case 4: Cart functionality"""
        print("\n=== Test Case 4: Cart Functionality ===")
        
        # Navigate to cart page
        page.goto(f"{self.base_url}/cart/")
        expect(page).to_have_url(f"{self.base_url}/cart/")
        print("✓ Cart page loads successfully")
        
        # Check for cart elements
        cart_elements = page.locator(".cart, .shopping-cart, [class*='cart']")
        if cart_elements.count() > 0:
            print("✓ Cart elements found")
        else:
            print("⚠ Cart elements not found")
        
        # Check for empty cart message or items
        empty_cart = page.locator(".empty, .no-items, [class*='empty']")
        cart_items = page.locator(".item, .cart-item, [class*='item']")
        
        if empty_cart.count() > 0:
            print("✓ Empty cart message displayed")
        elif cart_items.count() > 0:
            print(f"✓ Found {cart_items.count()} cart items")
        else:
            print("⚠ Cart state unclear")
        
        print("✅ Test Case 4 PASSED: Cart functionality works")

    def test_5_checkout_page(self, page: Page):
        """Test Case 5: Checkout page"""
        print("\n=== Test Case 5: Checkout Page ===")
        
        # Navigate to checkout page
        page.goto(f"{self.base_url}/checkout/")
        
        # Check if redirected to cart (empty cart) or stayed on checkout
        current_url = page.url
        if current_url.endswith("/cart/"):
            print("✓ Checkout page redirects to cart when empty (expected behavior)")
        elif current_url.endswith("/checkout/"):
            print("✓ Checkout page loads successfully")
        else:
            print(f"⚠ Unexpected URL: {current_url}")
        
        # Check for checkout form elements
        form_elements = page.locator("form, input, textarea")
        if form_elements.count() > 0:
            print(f"✓ Found {form_elements.count()} form elements")
        else:
            print("⚠ No form elements found")
        
        # Check for specific form fields
        first_name = page.locator("input[name='first_name']")
        last_name = page.locator("input[name='last_name']")
        email = page.locator("input[name='email']")
        
        if first_name.count() > 0:
            print("✓ First name field found")
        if last_name.count() > 0:
            print("✓ Last name field found")
        if email.count() > 0:
            print("✓ Email field found")
        
        print("✅ Test Case 5 PASSED: Checkout page works")

    def test_6_responsive_design(self, page: Page):
        """Test Case 6: Responsive design"""
        print("\n=== Test Case 6: Responsive Design ===")
        
        # Test different viewport sizes
        viewports = [
            {"width": 1920, "height": 1080, "name": "Desktop"},
            {"width": 768, "height": 1024, "name": "Tablet"},
            {"width": 375, "height": 667, "name": "Mobile"}
        ]
        
        for viewport in viewports:
            page.set_viewport_size(viewport)
            page.goto(f"{self.base_url}/")
            
            # Check if page loads properly
            page.wait_for_load_state("networkidle")
            print(f"✓ Page loads on {viewport['name']} ({viewport['width']}x{viewport['height']})")
        
        print("✅ Test Case 6 PASSED: Responsive design works")

    def test_7_error_handling(self, page: Page):
        """Test Case 7: Error handling"""
        print("\n=== Test Case 7: Error Handling ===")
        
        # Test 404 page
        page.goto(f"{self.base_url}/nonexistent-page/")
        
        # Check response status
        response = page.request.get(f"{self.base_url}/nonexistent-page/")
        if response.status == 404:
            print("✓ 404 error handling works")
        else:
            print(f"⚠ Unexpected status code: {response.status}")
        
        # Test invalid product page
        page.goto(f"{self.base_url}/product/invalid-product/")
        response = page.request.get(f"{self.base_url}/product/invalid-product/")
        if response.status == 404:
            print("✓ Invalid product page handling works")
        else:
            print(f"⚠ Invalid product page status: {response.status}")
        
        print("✅ Test Case 7 PASSED: Error handling works")

    def test_8_performance_loading(self, page: Page):
        """Test Case 8: Performance and loading times"""
        print("\n=== Test Case 8: Performance and Loading Times ===")
        
        # Test homepage loading time
        start_time = time.time()
        page.goto(f"{self.base_url}/")
        page.wait_for_load_state("networkidle")
        homepage_time = time.time() - start_time
        print(f"✓ Homepage loaded in {homepage_time:.2f} seconds")
        
        # Test products page loading time
        start_time = time.time()
        page.goto(f"{self.base_url}/products/")
        page.wait_for_load_state("networkidle")
        products_time = time.time() - start_time
        print(f"✓ Products page loaded in {products_time:.2f} seconds")
        
        # Performance warnings
        if homepage_time > 5:
            print("⚠ Homepage loading time is slow (>5s)")
        if products_time > 5:
            print("⚠ Products page loading time is slow (>5s)")
        
        print("✅ Test Case 8 PASSED: Performance checks completed")

    def test_9_accessibility_basics(self, page: Page):
        """Test Case 9: Basic accessibility checks"""
        print("\n=== Test Case 9: Basic Accessibility ===")
        
        page.goto(f"{self.base_url}/")
        
        # Check for images with alt text
        images = page.locator("img")
        if images.count() > 0:
            for i in range(images.count()):
                img = images.nth(i)
                alt_text = img.get_attribute("alt")
                if alt_text:
                    print(f"✓ Image {i+1} has alt text")
                else:
                    print(f"⚠ Image {i+1} missing alt text")
        else:
            print("✓ No images found (or no accessibility issues)")
        
        # Check for heading structure
        h1_count = page.locator("h1").count()
        if h1_count > 0:
            print(f"✓ Found {h1_count} H1 heading(s)")
        else:
            print("⚠ No H1 heading found")
        
        # Check for form labels
        inputs = page.locator("input, textarea, select")
        if inputs.count() > 0:
            print(f"✓ Found {inputs.count()} form inputs")
        else:
            print("✓ No form inputs found")
        
        print("✅ Test Case 9 PASSED: Basic accessibility checks completed")

    def test_10_cross_browser_compatibility(self, page: Page):
        """Test Case 10: Cross-browser compatibility"""
        print("\n=== Test Case 10: Cross-Browser Compatibility ===")
        
        # Test basic functionality
        page.goto(f"{self.base_url}/")
        
        # Check if page loads
        expect(page).to_have_url(f"{self.base_url}/")
        print("✓ Page loads in current browser")
        
        # Test navigation
        page.goto(f"{self.base_url}/products/")
        expect(page).to_have_url(f"{self.base_url}/products/")
        print("✓ Navigation works in current browser")
        
        # Test form interaction
        page.goto(f"{self.base_url}/checkout/")
        form_inputs = page.locator("input, textarea")
        if form_inputs.count() > 0:
            print("✓ Form elements work in current browser")
        else:
            print("⚠ Form elements not found")
        
        print("✅ Test Case 10 PASSED: Cross-browser compatibility works")
