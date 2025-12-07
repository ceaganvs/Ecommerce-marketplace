from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Store(models.Model):
    """Stores created by vendors"""
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (by {self.vendor.username})"

    class Meta:
        permissions = [
            ("manage_store", "Can manage stores"),
        ]


class Product(models.Model):
    """Products in stores"""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

    class Meta:
        permissions = [
            ("manage_products", "Can manage products"),
        ]


class Order(models.Model):
    """Orders placed by buyers"""
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username}"


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of purchase

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"


class Review(models.Model):
    """Product reviews by buyers"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField()
    verified = models.BooleanField(default=False)  # True if buyer purchased this product
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        verified_text = "Verified" if self.verified else "Unverified"
        return f"{verified_text} Review by {self.buyer.username} - {self.rating} stars"

    class Meta:
        unique_together = ('product', 'buyer')  # One review per buyer per product


class ResetToken(models.Model):
    """Password reset tokens"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expiry_date

    def __str__(self):
        return f"ResetToken for {self.user.username}"

