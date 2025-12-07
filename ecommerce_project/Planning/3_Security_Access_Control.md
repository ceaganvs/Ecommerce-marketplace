# Keeping the System Secure

## Logging In

### Signing Up
- Ask for: username, email, password, vendor or buyer
- Password needs to be at least 8 characters
- Don't save passwords as plain text - encrypt them
- Django does this automatically

### Logging In
- Check if password matches
- Create a session to keep user logged in
- Add security token to forms

## Who Can Do What

### Vendors Can:
- Make and edit their own stores
- Add and edit products in their stores
- Can't buy things
- Can't see other vendors' stores

### Buyers Can:
- Look at all products
- Add to cart and buy
- Write reviews
- Can't make stores

### Visitors Can:
- Just look at products
- Need to sign up to do more

## Checking Permissions

Before letting someone do something, check:
- Are they logged in?
- Are they a vendor or buyer?
- If editing a store, do they own it?

If they shouldn't access something:
- Show "Access Denied" message
- Send them back to safe page

## Security Measures

### 1. CSRF Protection
- All POST forms include `{% csrf_token %}`
- Django validates token on submission
- Prevents cross-site request forgery attacks

### 2. SQL Injection Prevention
- Never use raw SQL queries
- Django ORM parameterizes all queries automatically
- User input never directly concatenated into queries

### 3. XSS Protection
- Django auto-escapes template variables
- `{{ user_input }}` is safe by default
- Only use `|safe` filter when absolutely necessary

### 4. Password Security
- Passwords hashed with PBKDF2 + SHA256
- Salt automatically added
- Never logged or displayed
- Password reset uses secure tokens

### 5. Secure Password Reset
- Token generated with `secrets.token_urlsafe(32)`
- Token hashed with SHA-1 before database storage
- 30-minute expiration window
- Single-use tokens (marked as used)
- No user info leaked if email doesn't exist

### 6. Email Security
- Don't reveal if email exists in system
- Same message for valid/invalid emails during reset
- Prevents user enumeration attacks

### 7. Session Security
- Cookies marked as HttpOnly
- CSRF cookie with SameSite=Lax
- Session data server-side only
- Automatic session expiry

## Security Protections

### Form Security
- Add special token to forms (CSRF protection)
- Django checks token when form submitted
- Stops fake form submissions

### Password Security
- Passwords encrypted before saving
- Never show passwords anywhere
- Password reset links expire after 30 minutes
- Can only use reset link once

### Input Checking
- Make sure prices are numbers
- Make sure stock isn't negative
- Check all form data before saving
- Show error if something's wrong

### Don't Show Sensitive Info
- Don't tell hackers if username exists
- Keep error messages simple
- Don't show database errors to users

## What We Save

**We keep:**
- Encrypted passwords
- Email addresses  
- Orders people made
- Shopping cart (temporary)

**We don't keep:**
- Actual passwords (only encrypted version)
- Credit card numbers (not doing payments yet)


