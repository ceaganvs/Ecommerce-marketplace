"""
API URL Configuration
Following REST API best practices for resource naming and routing
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import StoreViewSet, ProductViewSet, ReviewViewSet, VendorViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'vendors', VendorViewSet, basename='vendor')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
