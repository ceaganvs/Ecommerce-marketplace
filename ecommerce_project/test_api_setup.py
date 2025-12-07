"""
Test script to verify API setup
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User, Group
from marketplace.api_views import StoreViewSet, ProductViewSet, ReviewViewSet
from marketplace.models import Store, Product, Review

def test_api_setup():
    """Test that API views and serializers are properly configured"""
    
    print("Testing API Setup...")
    print("=" * 60)
    
    # Test 1: Check if viewsets are importable
    print("\n✓ ViewSets imported successfully")
    print(f"  - StoreViewSet: {StoreViewSet}")
    print(f"  - ProductViewSet: {ProductViewSet}")
    print(f"  - ReviewViewSet: {ReviewViewSet}")
    
    # Test 2: Check REST Framework configuration
    from django.conf import settings
    if 'rest_framework' in settings.INSTALLED_APPS:
        print("\n✓ Django REST Framework is installed")
    else:
        print("\n✗ Django REST Framework is NOT installed")
        return False
    
    # Test 3: Check models
    print("\n✓ Models are accessible:")
    print(f"  - Store model: {Store}")
    print(f"  - Product model: {Product}")
    print(f"  - Review model: {Review}")
    
    # Test 4: Create test factory
    factory = APIRequestFactory()
    print("\n✓ API Request Factory created")
    
    # Test 5: Check URL routing
    try:
        from marketplace.api_urls import router
        print("\n✓ API Router configured")
        print(f"  Registered viewsets: {list(router.registry)}")
    except Exception as e:
        print(f"\n✗ Error importing API URLs: {e}")
        return False
    
    # Test 6: Check serializers
    try:
        from marketplace.serializers import (
            StoreSerializer, ProductSerializer, ReviewSerializer
        )
        print("\n✓ Serializers imported successfully")
        print(f"  - StoreSerializer: {StoreSerializer}")
        print(f"  - ProductSerializer: {ProductSerializer}")
        print(f"  - ReviewSerializer: {ReviewSerializer}")
    except Exception as e:
        print(f"\n✗ Error importing serializers: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All API components are properly configured!")
    print("\nNext steps:")
    print("1. Run: python manage.py makemigrations")
    print("2. Run: python manage.py migrate")
    print("3. Run: python setup_groups.py")
    print("4. Create test users (vendors and buyers)")
    print("5. Run: python manage.py runserver")
    print("6. Visit: http://localhost:8000/api/")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        test_api_setup()
    except Exception as e:
        print(f"\n✗ Error during setup test: {e}")
        import traceback
        traceback.print_exc()
