import pytest
import os
import sys
import django
from django.test import TestCase

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_poc.settings')
django.setup()

# Import Django models after setup
from django.contrib.auth.models import User
from django.core.management import call_command
from shop.models import Category, Product, Cart, CartItem, Order, OrderItem

@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Set up test database with sample data"""
    with django_db_blocker.unblock():
        # Create test data
        call_command('loaddata', 'shop/fixtures/test_data.json', verbosity=0)
        
        # Create test categories
        category1 = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Electronic devices and gadgets"
        )
        category2 = Category.objects.create(
            name="Clothing",
            slug="clothing", 
            description="Fashion and apparel"
        )
        
        # Create test products
        product1 = Product.objects.create(
            name="Test Laptop",
            slug="test-laptop",
            description="A high-quality test laptop",
            short_description="Test Laptop",
            price=999.99,
            category=category1,
            stock=10,
            is_featured=True,
            is_active=True
        )
        
        product2 = Product.objects.create(
            name="Test T-Shirt",
            slug="test-tshirt",
            description="A comfortable test t-shirt",
            short_description="Test T-Shirt",
            price=29.99,
            category=category2,
            stock=50,
            is_featured=True,
            is_active=True
        )
        
        product3 = Product.objects.create(
            name="Test Phone",
            slug="test-phone",
            description="A modern test smartphone",
            short_description="Test Phone",
            price=699.99,
            category=category1,
            stock=5,
            is_featured=False,
            is_active=True
        )

@pytest.fixture
def test_user():
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def test_category():
    """Create a test category"""
    return Category.objects.create(
        name="Test Category",
        slug="test-category",
        description="A test category"
    )

@pytest.fixture
def test_product(test_category):
    """Create a test product"""
    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        description="A test product description",
        short_description="Test Product",
        price=99.99,
        category=test_category,
        stock=25,
        is_featured=True,
        is_active=True
    )

@pytest.fixture
def test_cart(test_user):
    """Create a test cart"""
    return Cart.objects.create(user=test_user)

@pytest.fixture
def test_cart_item(test_cart, test_product):
    """Create a test cart item"""
    return CartItem.objects.create(
        cart=test_cart,
        product=test_product,
        quantity=2
    )

@pytest.fixture
def test_order(test_user):
    """Create a test order"""
    return Order.objects.create(
        user=test_user,
        first_name="Test",
        last_name="User",
        email="test@example.com",
        address="123 Test Street",
        postal_code="12345",
        city="Test City",
        status="pending"
    )

@pytest.fixture
def test_order_item(test_order, test_product):
    """Create a test order item"""
    return OrderItem.objects.create(
        order=test_order,
        product=test_product,
        price=test_product.price,
        quantity=1
    )
