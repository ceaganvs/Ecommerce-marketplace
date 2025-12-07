# What the System Needs to Do

## Basic Idea
A website where some people sell stuff and other people buy it.

## Who Will Use It

### Vendors (Sellers)
People who want to sell things online.

**What they can do:**
- Sign up as a vendor
- Make a store
- Add products (with name, description, price, how many in stock)
- Change or delete products
- See their own stuff

### Buyers (Customers)
People who want to buy things.

**What they can do:**
- Sign up as a buyer
- Look at products
- Put items in a cart
- Buy the items
- Get an email after buying
- Write reviews

### Visitors
People just browsing without an account.

**What they can do:**
- Look at products
- See reviews
- Sign up if they want

## Main Features Needed

### Login Stuff
- Register (pick if you're a vendor or buyer)
- Log in and log out
- Reset password if you forget it
- Keep people logged in while browsing

### For Vendors
- Make stores
- Add products to stores
- Edit products
- Delete products
- Only see and edit their own stuff

### For Buyers
- Browse products
- Add to cart
- Checkout and pay
- Get email confirmation
- Leave reviews (marked "verified" if they bought it)

### Emails
- Send password reset links
- Send order confirmations after purchase

## What Data We Need to Store

1. **Users**
   - Username, email, password
   - If they're a vendor or buyer

2. **Stores**
   - Store name and description
   - Who owns it

3. **Products**
   - Name, description, price, stock amount
   - Which store it belongs to

4. **Orders**
   - Who bought it
   - Total price
   - When they bought it

5. **Order Items**
   - What products were in the order
   - How many of each

6. **Reviews**
   - Rating and comment
   - Who wrote it and for which product
   - If they actually bought it (verified)

7. **Password Reset Tokens**
   - Link for resetting password
   - Expires after 30 minutes

## Important Things

- Passwords must be encrypted
- Vendors only see their own stores
- Buyers can't create stores
- Cart stays filled while browsing
- Show clear error messages
- Works on phones and computers
- Easy to use
