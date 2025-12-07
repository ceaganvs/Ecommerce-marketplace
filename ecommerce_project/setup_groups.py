"""
Setup script to create Vendor and Buyer groups
Run with: python manage.py shell < setup_groups.py
"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from marketplace.models import Store, Product

# Create Vendors group
vendors_group, created = Group.objects.get_or_create(name='Vendors')
if created:
    print("Created Vendors group")
    # Add permissions for vendors
    store_ct = ContentType.objects.get_for_model(Store)
    product_ct = ContentType.objects.get_for_model(Product)
    
    # Store permissions
    for perm in Permission.objects.filter(content_type=store_ct):
        vendors_group.permissions.add(perm)
    
    # Product permissions
    for perm in Permission.objects.filter(content_type=product_ct):
        vendors_group.permissions.add(perm)
    
    print("Added permissions to Vendors group")
else:
    print("Vendors group already exists")

# Create Buyers group
buyers_group, created = Group.objects.get_or_create(name='Buyers')
if created:
    print("Created Buyers group")
else:
    print("Buyers group already exists")

print("\nGroups setup complete!")
print("Vendors can: manage stores and products")
print("Buyers can: view products, add to cart, checkout, leave reviews")
