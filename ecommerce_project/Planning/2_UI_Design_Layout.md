# How the Website Should Look

## Keep It Simple
- Don't add too much stuff on one page
- Same menu on every page
- Easy to read
- Works on phones

## Colors
- Dark gray for headers
- White backgrounds
- Green for prices
- Red for errors
- Green for success messages

## Menu at Top
Every page has links at the top:
- Vendors see: My Stores
- Buyers see: Cart
- Everyone sees: Home, Login/Logout

## Main Pages

### Home Page
Shows all products in boxes with:
- Product name
- Price
- How many left
- Which store
- Button to see more details

### Register Page
Form to sign up:
- Username
- Email  
- Password
- Choose: Vendor or Buyer

### Login Page
Simple form:
- Username
- Password
- Link to reset password

### Vendor Pages

**My Stores:**
- List of your stores
- Button to create new store
- Edit and delete buttons

**Store Products:**
- Table of products in that store
- Shows name, price, stock
- Add new product button
- Edit and delete for each product

### Buyer Pages

**Product Details:**
- Name and price
- Description
- Add to cart button with quantity
- Reviews below
- Stars showing rating
- Checkmark if review is verified

**Shopping Cart:**
- List of items
- Price for each
- Quantity
- Total price
- Checkout button
- Remove item buttons

**Order Success:**
- "Thank you" message
- Order number
- "Email sent" notice

## How Forms Work
- Label above each box
- Mark required fields
- Show errors at top in red
- Keep what user typed if there's an error
- Clear submit button

## Steps Users Take

**Vendors:**
1. Register and pick "Vendor"
2. Go to My Stores
3. Create a store
4. Add products to it
5. Can edit or delete anytime

**Buyers:**
1. Register and pick "Buyer"
2. Look at products
3. Click one to see details
4. Add to cart
5. Go to cart
6. Checkout
7. Get confirmation

## Error Messages
Keep them simple:
- "Wrong username or password"
- "Not enough items in stock"
- "Please fill in all fields"
- "Price must be a number"

## Loading States
- Show simple "Processing..." text during checkout
- Django's default error pages for 404/500
- Form submission: disable button to prevent double-click
