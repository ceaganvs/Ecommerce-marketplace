from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils import timezone
from django.db.models import Sum, F
from datetime import timedelta
from hashlib import sha1
import secrets

from .models import Store, Product, Order, OrderItem, Review, ResetToken


# ==================== AUTHENTICATION VIEWS ====================

def register_user(request):
    """Register new users as Vendor or Buyer"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')  # 'vendor' or 'buyer'

        if User.objects.filter(username=username).exists():
            return render(request, 'marketplace/register.html', {
                'error': 'Username already exists'
            })

        # Create user
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # Assign to appropriate group
        if user_type == 'vendor':
            group, _ = Group.objects.get_or_create(name='Vendors')
            user.groups.add(group)
        else:
            group, _ = Group.objects.get_or_create(name='Buyers')
            user.groups.add(group)
        
        user.save()
        login(request, user)
        
        return redirect('marketplace:home')
    
    return render(request, 'marketplace/register.html')


def login_user(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('marketplace:home')
        else:
            return render(request, 'marketplace/login.html', {
                'error': 'Invalid credentials'
            })
    
    return render(request, 'marketplace/login.html')


def logout_user(request):
    """User logout"""
    logout(request)
    return redirect('marketplace:login')


def request_password_reset(request):
    """Request password reset email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            # Generate token
            token = secrets.token_urlsafe(32)
            expiry_date = timezone.now() + timedelta(minutes=30)
            hashed_token = sha1(token.encode()).hexdigest()
            
            # Save token
            ResetToken.objects.create(
                user=user,
                token=hashed_token,
                expiry_date=expiry_date
            )
            
            # Send email
            reset_url = request.build_absolute_uri(
                reverse('marketplace:password_reset', args=[token])
            )
            
            email_message = EmailMessage(
                subject='Password Reset',
                body=f'Click here to reset your password: {reset_url}',
                from_email='noreply@marketplace.com',
                to=[user.email]
            )
            email_message.send()
            
            return render(request, 'marketplace/reset_email_sent.html')
        
        except User.DoesNotExist:
            # Don't reveal if email exists
            return render(request, 'marketplace/reset_email_sent.html')
    
    return render(request, 'marketplace/request_password_reset.html')


def password_reset(request, token):
    """Reset password with token"""
    hashed_token = sha1(token.encode()).hexdigest()
    
    try:
        reset_token = ResetToken.objects.get(token=hashed_token, used=False)
        
        if reset_token.is_expired():
            reset_token.delete()
            return render(request, 'marketplace/password_reset_expired.html')
        
        if request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            if password != password_confirm:
                return render(request, 'marketplace/password_reset.html', {
                    'error': 'Passwords do not match',
                    'token': token
                })
            
            # Update password
            user = reset_token.user
            user.set_password(password)
            user.save()
            
            # Mark token as used
            reset_token.used = True
            reset_token.save()
            
            return redirect('marketplace:login')
        
        return render(request, 'marketplace/password_reset.html', {'token': token})
    
    except ResetToken.DoesNotExist:
        return render(request, 'marketplace/password_reset_invalid.html')


# ==================== HOME & PRODUCT BROWSING ====================

def home(request):
    """Home page showing all products"""
    products = Product.objects.all().select_related('store')
    return render(request, 'marketplace/home.html', {'products': products})


def product_detail(request, product_id):
    """View product details and reviews"""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all().order_by('-created_at')
    
    # Check if user has purchased this product
    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(
            order__buyer=request.user,
            product=product
        ).exists()
    
    return render(request, 'marketplace/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'has_purchased': has_purchased
    })


# ==================== VENDOR VIEWS ====================

@login_required
def my_stores(request):
    """List vendor's stores"""
    if not request.user.groups.filter(name='Vendors').exists():
        return HttpResponseForbidden("Only vendors can access this page")
    
    stores = request.user.stores.all()
    return render(request, 'marketplace/my_stores.html', {'stores': stores})


@login_required
def create_store(request):
    """Create a new store"""
    if not request.user.groups.filter(name='Vendors').exists():
        return HttpResponseForbidden("Only vendors can create stores")
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        store = Store.objects.create(
            vendor=request.user,
            name=name,
            description=description
        )
        
        return redirect('marketplace:my_stores')
    
    return render(request, 'marketplace/create_store.html')


@login_required
def edit_store(request, store_id):
    """Edit a store"""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    
    if request.method == 'POST':
        store.name = request.POST.get('name')
        store.description = request.POST.get('description')
        store.save()
        
        return redirect('marketplace:my_stores')
    
    return render(request, 'marketplace/edit_store.html', {'store': store})


@login_required
def delete_store(request, store_id):
    """Delete a store"""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    
    if request.method == 'POST':
        store.delete()
        return redirect('marketplace:my_stores')
    
    return render(request, 'marketplace/delete_store.html', {'store': store})


@login_required
def store_products(request, store_id):
    """List products in a store"""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    products = store.products.all()
    
    return render(request, 'marketplace/store_products.html', {
        'store': store,
        'products': products
    })


@login_required
def create_product(request, store_id):
    """Add product to store"""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    
    if request.method == 'POST':
        try:
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            
            # Validate price and stock
            if not price or float(price) < 0:
                return render(request, 'marketplace/create_product.html', {
                    'store': store,
                    'error': 'Price must be a valid positive number'
                })
            
            if not stock or int(stock) < 0:
                return render(request, 'marketplace/create_product.html', {
                    'store': store,
                    'error': 'Stock must be a valid positive number'
                })
            
            product = Product.objects.create(
                store=store,
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                price=float(price),
                stock=int(stock)
            )
            
            return redirect('marketplace:store_products', store_id=store.id)
        except (ValueError, TypeError) as e:
            return render(request, 'marketplace/create_product.html', {
                'store': store,
                'error': 'Invalid price or stock value. Please enter valid numbers.'
            })
    
    return render(request, 'marketplace/create_product.html', {'store': store})


@login_required
def edit_product(request, product_id):
    """Edit a product"""
    product = get_object_or_404(Product, id=product_id, store__vendor=request.user)
    
    if request.method == 'POST':
        try:
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            
            # Validate price and stock
            if not price or float(price) < 0:
                return render(request, 'marketplace/edit_product.html', {
                    'product': product,
                    'error': 'Price must be a valid positive number'
                })
            
            if not stock or int(stock) < 0:
                return render(request, 'marketplace/edit_product.html', {
                    'product': product,
                    'error': 'Stock must be a valid positive number'
                })
            
            product.name = request.POST.get('name')
            product.description = request.POST.get('description')
            product.price = float(price)
            product.stock = int(stock)
            product.save()
            
            return redirect('marketplace:store_products', store_id=product.store.id)
        except (ValueError, TypeError) as e:
            return render(request, 'marketplace/edit_product.html', {
                'product': product,
                'error': 'Invalid price or stock value. Please enter valid numbers.'
            })
    
    return render(request, 'marketplace/edit_product.html', {'product': product})


@login_required
def delete_product(request, product_id):
    """Delete a product"""
    product = get_object_or_404(Product, id=product_id, store__vendor=request.user)
    store_id = product.store.id
    
    if request.method == 'POST':
        product.delete()
        return redirect('marketplace:store_products', store_id=store_id)
    
    return render(request, 'marketplace/delete_product.html', {'product': product})


# ==================== CART & CHECKOUT ====================

def view_cart(request):
    """View shopping cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
        except Product.DoesNotExist:
            pass
    
    return render(request, 'marketplace/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect('marketplace:view_cart')


def remove_from_cart(request, product_id):
    """Remove product from cart"""
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('marketplace:view_cart')


@login_required
def checkout(request):
    """Checkout and create order"""
    if not request.user.groups.filter(name='Buyers').exists():
        return HttpResponseForbidden("Only buyers can checkout")
    
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('marketplace:view_cart')
    
    # Calculate total and create order
    total = 0
    order_items = []
    
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        
        if product.stock < quantity:
            return render(request, 'marketplace/cart.html', {
                'error': f'Not enough stock for {product.name}'
            })
        
        subtotal = product.price * quantity
        total += subtotal
        order_items.append({
            'product': product,
            'quantity': quantity,
            'price': product.price
        })
    
    # Create order
    order = Order.objects.create(
        buyer=request.user,
        total_price=total
    )
    
    # Create order items and update stock
    for item in order_items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price']
        )
        
        # Reduce stock
        product = item['product']
        product.stock -= item['quantity']
        product.save()
    
    # Send invoice email
    send_invoice_email(order)
    
    # Clear cart
    request.session['cart'] = {}
    request.session.modified = True
    
    return render(request, 'marketplace/order_success.html', {'order': order})


def send_invoice_email(order):
    """Send invoice to buyer"""
    items_text = "\n".join([
        f"{item.quantity}x {item.product.name} - ${item.price} = ${item.quantity * item.price}"
        for item in order.items.all()
    ])
    
    body = f"""
    Order Invoice #{ order.id}
    
    Items:
    {items_text}
    
    Total: ${order.total_price}
    
    Thank you for your purchase!
    """
    
    email = EmailMessage(
        subject=f'Order Invoice #{order.id}',
        body=body,
        from_email='noreply@marketplace.com',
        to=[order.buyer.email]
    )
    email.send()


# ==================== REVIEWS ====================

@login_required
def add_review(request, product_id):
    """Add a review for a product"""
    if not request.user.groups.filter(name='Buyers').exists():
        return HttpResponseForbidden("Only buyers can leave reviews")
    
    product = get_object_or_404(Product, id=product_id)
    
    # Check if already reviewed
    if Review.objects.filter(product=product, buyer=request.user).exists():
        return redirect('marketplace:product_detail', product_id=product_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Check if user has purchased this product
        has_purchased = OrderItem.objects.filter(
            order__buyer=request.user,
            product=product
        ).exists()
        
        Review.objects.create(
            product=product,
            buyer=request.user,
            rating=rating,
            comment=comment,
            verified=has_purchased
        )
        
        return redirect('marketplace:product_detail', product_id=product_id)
    
    return render(request, 'marketplace/add_review.html', {'product': product})

