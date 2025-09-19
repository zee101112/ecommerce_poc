#!/usr/bin/env python
"""
Setup script for Ipswich Retail Shop Django E-commerce PoC
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_project():
    """Setup the Django project with migrations and sample data"""
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_poc.settings')
    django.setup()
    
    print("🚀 Setting up Ipswich Retail Shop E-commerce PoC...")
    
    # Run migrations
    print("\n📦 Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser (optional)
    print("\n👤 Creating superuser...")
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@ipswichretail.com', 'admin123')
            print("✅ Superuser created: username='admin', password='admin123'")
        else:
            print("ℹ️  Superuser already exists")
    except Exception as e:
        print(f"⚠️  Could not create superuser: {e}")
    
    # Populate sample data
    print("\n📊 Populating database with sample data...")
    execute_from_command_line(['manage.py', 'populate_data'])
    
    print("\n✅ Setup complete!")
    print("\n🎉 Your Django e-commerce PoC is ready!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000")
    print("3. Admin panel: http://127.0.0.1:8000/admin")
    print("4. Login with: admin / admin123")
    print("\n🔧 Features included:")
    print("• Home page with featured products")
    print("• Product listing with search and filters")
    print("• Product detail pages")
    print("• Shopping cart functionality")
    print("• Responsive Bootstrap design")
    print("• Django admin interface")

if __name__ == '__main__':
    setup_project()
