from django.contrib import admin
from .models import Store, Product, Order, OrderItem, Review, ResetToken

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'created_at')
    search_fields = ('name', 'vendor__username')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'stock')
    list_filter = ('store',)
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'total_price', 'created_at')
    list_filter = ('created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'buyer', 'rating', 'verified', 'created_at')
    list_filter = ('verified', 'rating')

@admin.register(ResetToken)
class ResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'expiry_date', 'used')

