from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('request-password-reset/', views.request_password_reset, name='request_password_reset'),
    path('password-reset/<str:token>/', views.password_reset, name='password_reset'),
    
    # Products
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Vendor - Stores
    path('my-stores/', views.my_stores, name='my_stores'),
    path('create-store/', views.create_store, name='create_store'),
    path('edit-store/<int:store_id>/', views.edit_store, name='edit_store'),
    path('delete-store/<int:store_id>/', views.delete_store, name='delete_store'),
    
    # Vendor - Products
    path('store/<int:store_id>/products/', views.store_products, name='store_products'),
    path('store/<int:store_id>/add-product/', views.create_product, name='create_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    
    # Cart & Checkout
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Reviews
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
]
