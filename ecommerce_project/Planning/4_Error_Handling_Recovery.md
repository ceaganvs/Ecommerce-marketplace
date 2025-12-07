# Error Handling & Recovery Plan

## Common Errors and How to Handle Them

### 1. User Input Errors
Users might enter wrong information in forms.

**Examples:**
- Typing letters in price field
- Entering negative numbers for stock
- Leaving required fields empty
- Wrong email format

**How to fix:**
- Check the input before saving
- Show a clear error message
- Let user fix it without losing other data
- Add basic validation to forms

### 2. Login Problems

**What can happen:**
- Wrong password
- Wrong username
- Session expired
- Trying to access pages without logging in

**What to do:**
- Show "Invalid credentials" message
- Redirect to login page when needed
- Don't reveal which part is wrong (security)
- Ask user to try again

### 3. Missing Items

**Problems:**
- Product deleted while in cart
- Store removed while viewing
- Item not found

**Solution:**
- Show "Not found" page
- Remove deleted items from cart
- Redirect back to home or product list
- Give helpful message

### 4. Stock Issues

**Scenarios:**
- Trying to buy more than available
- Product runs out during checkout
- Two people buying last item at same time

**Fix:**
- Check stock before completing order
- Show how many are available
- Update stock count after purchase
- Show clear error if not enough

### 5. Email Not Sending

**Possible reasons:**
- Email server problems
- Wrong email address
- Network issues

**What happens:**
- Order still goes through
- Save order details in database
- Show message that email might be delayed
- User can still see order confirmation on site

### 6. Cart Problems

**Issues:**
- Cart disappears (session expired)
- Product in cart gets deleted
- Cart has old items

**Handle by:**
- Check if items still exist
- Remove items that don't exist anymore
- Show message about removed items
- Let user continue with remaining items

### 7. Access Denied

**When it happens:**
- Buyer tries to create store
- Vendor tries to checkout
- User tries to edit someone else's store
- Not logged in user tries restricted action

**Response:**
- Show "Access Denied" message
- Explain why they can't do this
- Suggest what to do instead
- Provide link back to safe page

## Writing Good Error Messages

**Keep it simple:**
- "Price must be a number"
- "Not enough stock available"
- "Wrong username or password"
- "Item not found"

**Avoid technical terms:**
- Don't say "Error 500" or "Database error"
- Use plain English
- Be helpful, not scary

## How Users Can Fix Problems

### Vendors:
- Wrong price? → Click Edit button to fix it
- Wrong store name? → Edit or delete and start over
- Can't find something? → Go back to My Stores page

### Buyers:
- Out of stock? → Reduce quantity or remove item
- Removed item by accident? → Browse and add it again
- Cart empty? → Start shopping again

## Checking User Input

We check inputs in two places:

1. **In the form (HTML):**
   - Fields marked as required
   - Number fields only accept numbers
   - Prevents simple mistakes

2. **On the server (Django):**
   - Double-check everything
   - Make sure price is positive
   - Verify all required fields filled
   - This is the real security check

## Testing Different Errors

Try these to make sure errors are handled:

1. **Login errors:**
   - Try wrong password
   - Try wrong username
   - Leave fields empty

2. **Product errors:**
   - Enter negative price
   - Leave product name blank
   - Type letters in stock field

3. **Cart errors:**
   - Try to buy more than available
   - Try checkout with empty cart
   - Delete a product that's in someone's cart

4. **Access errors:**
   - Try buyer accessing vendor pages
   - Try editing another person's store
   - Try checkout without logging in

## When Things Go Really Wrong

### Database problems:
- Keep regular backups
- Can restore if needed
- Test backups to make sure they work

### Server crashes:
- Just restart it
- User sessions are saved in database
- Users might need to login again

### Email server down:
- Orders still work
- Save order info in database
- Can send emails later manually

## Making Error Messages Helpful

When showing an error:
1. Say what went wrong
2. Tell user what to do next
3. Keep it short and simple

Example:
"Not enough stock for this item. Only 5 available. Please reduce your quantity or remove the item."

## Things to Remember

- Always check user input before saving
- Show clear, helpful messages
- Don't show technical errors to users
- Keep the system working even if one part fails
- Make it easy for users to fix mistakes
- Test error cases, not just successful ones

## User Communication

### During errors:
1. Acknowledge the problem
2. Explain what happened (simply)
3. Suggest next steps
4. Provide way to contact support (future)

### Example flow:
```
User tries to checkout with out-of-stock item:

"Sorry, we don't have enough stock for Laptop.
Only 5 available, but you requested 10.

You can:
- Reduce quantity to 5
- Remove item from cart
- Continue shopping

Your other items are still in your cart."
```
