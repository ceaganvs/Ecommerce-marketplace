# API Serializers

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Store, Product, Review, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id',
            'product',
            'product_name',
            'buyer',
            'buyer_username',
            'rating',
            'comment',
            'verified',
            'created_at'
        ]
        read_only_fields = ['id', 'buyer', 'verified', 'created_at']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    
    def create(self, validated_data):
        validated_data['buyer'] = self.context['request'].user
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Products
    - Includes store information
    - Shows average rating and review count
    - Links to related reviews
    """
    store_name = serializers.CharField(source='store.name', read_only=True)
    vendor_name = serializers.CharField(source='store.vendor.username', read_only=True)
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    reviews = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='review-detail'
    )
    
    class Meta:
        model = Product
        fields = [
            'id',
            'store',
            'store_name',
            'vendor_name',
            'name',
            'description',
            'price',
            'stock',
            'image',
            'reviews_count',
            'average_rating',
            'reviews',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_reviews_count(self, obj):
        """Get total number of reviews"""
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        """Calculate average rating from all reviews"""
        reviews = obj.reviews.all()
        if reviews.exists():
            avg = sum(r.rating for r in reviews) / len(reviews)
            return round(avg, 2)
        return None
    
    def validate_price(self, value):
        """Ensure price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value
    
    def validate_stock(self, value):
        """Ensure stock is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value


class StoreSerializer(serializers.ModelSerializer):
    """
    Serializer for Stores
    - Includes vendor information
    - Shows product count
    - Nested products list (optional)
    """
    vendor = UserSerializer(read_only=True)
    vendor_username = serializers.CharField(source='vendor.username', read_only=True)
    products_count = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Store
        fields = [
            'id',
            'vendor',
            'vendor_username',
            'name',
            'description',
            'logo',
            'products_count',
            'products',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'vendor', 'created_at', 'updated_at']
    
    def get_products_count(self, obj):
        """Get total number of products in store"""
        return obj.products.count()
    
    def create(self, validated_data):
        """Auto-set vendor from request user"""
        validated_data['vendor'] = self.context['request'].user
        return super().create(validated_data)


class StoreListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing stores
    - Excludes nested products for better performance
    - Used in list views
    """
    vendor_username = serializers.CharField(source='vendor.username', read_only=True)
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Store
        fields = [
            'id',
            'vendor_username',
            'name',
            'description',
            'logo',
            'products_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_products_count(self, obj):
        """Get total number of products in store"""
        return obj.products.count()


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing products
    - Excludes nested reviews for better performance
    - Used in list views
    """
    store_name = serializers.CharField(source='store.name', read_only=True)
    vendor_name = serializers.CharField(source='store.vendor.username', read_only=True)
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'store_name',
            'vendor_name',
            'name',
            'description',
            'price',
            'stock',
            'image',
            'reviews_count',
            'average_rating',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_reviews_count(self, obj):
        """Get total number of reviews"""
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        """Calculate average rating from all reviews"""
        reviews = obj.reviews.all()
        if reviews.exists():
            avg = sum(r.rating for r in reviews) / len(reviews)
            return round(avg, 2)
        return None


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for items within an order"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']
        read_only_fields = ['id', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Orders"""
    buyer = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'items', 'total_price', 'created_at']
        read_only_fields = ['id', 'buyer', 'total_price', 'created_at']
