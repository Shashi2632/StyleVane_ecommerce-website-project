from .models import CartItem, Products

def cart_count(request):
    cart_items = []
    if request.user.is_authenticated:
        # User is logged in, fetch cart items for the logged-in user
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        # User is not logged in, handle the cart using sessions
        cart = request.session.get('cart', {})
        for product_id, cart_item_data in cart.items():
            try:
                product = Products.objects.get(id=int(product_id))
                cart_item = {
                    'product': product,
                    'quantity': cart_item_data['quantity'],
                }
                cart_items.append(cart_item)
            except Products.DoesNotExist:
                # Handle cases where the product doesn't exist
                pass

    cart_count = len(cart_items)

    return {'cart_count': cart_count}

def username(request):
    username = request.session.get('username', None)
    return {'username': username}
