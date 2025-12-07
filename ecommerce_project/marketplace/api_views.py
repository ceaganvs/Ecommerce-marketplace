# REST API views for marketplace

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from .models import Store, Product, Review, Order, OrderItem
from .serializers import (
    StoreSerializer, StoreListSerializer,
    ProductSerializer, ProductListSerializer,
    ReviewSerializer, UserSerializer,
    OrderSerializer
)


# Custom Permissions

class IsVendorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (request.user and 
                request.user.is_authenticated and 
                request.user.groups.filter(name='Vendors').exists())


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if isinstance(obj, Store):
            return obj.vendor == request.user
        elif isinstance(obj, Product):
            return obj.store.vendor == request.user
        elif isinstance(obj, Review):
            return obj.buyer == request.user
        
        return False


class IsBuyerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (request.user and 
                request.user.is_authenticated and 
                request.user.groups.filter(name='Buyers').exists())


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all().select_related('vendor').prefetch_related('products')
    permission_classes = [IsVendorOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vendor__username']
    search_fields = ['name', 'description', 'vendor__username']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return StoreListSerializer
        return StoreSerializer
    
    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        store = self.get_object()
        products = store.products.all()
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('store__vendor').prefetch_related('reviews')
    permission_classes = [IsVendorOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['store', 'store__vendor__username']
    search_fields = ['name', 'description', 'store__name']
    ordering_fields = ['created_at', 'price', 'stock', 'name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    def perform_create(self, serializer):
        store = serializer.validated_data.get('store')
        if store.vendor != self.request.user:
            raise permissions.PermissionDenied("You can only add products to your own stores")
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all().select_related('buyer')
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('product', 'buyer')
    permission_classes = [IsBuyerOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'buyer__username', 'rating', 'verified']
    search_fields = ['comment', 'product__name']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(groups__name='Vendors').prefetch_related('stores')
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email']
    ordering = ['username']
    
    @action(detail=True, methods=['get'])
    def stores(self, request, pk=None):
        vendor = self.get_object()
        stores = vendor.stores.all().prefetch_related('products')
        serializer = StoreListSerializer(stores, many=True, context={'request': request})
        return Response(serializer.data)
