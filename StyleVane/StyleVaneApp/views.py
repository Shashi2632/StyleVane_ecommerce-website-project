from django.shortcuts import render,redirect, get_object_or_404
from StyleVaneApp.models import Products, Blogs, CartItem, Order, OrderDetail
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, Page , EmptyPage, PageNotAnInteger
from django.db import transaction
# Create your views here.


def index(request):
    productData = Products.objects.all()
    data = {
            'productData': productData,
            }
    return render(request, 'index.html', data)

def shop(request):
    productData = Products.objects.all()
    pagi = Paginator(productData,6)
    page_num = request.GET.get('page')
    productData1 = pagi.get_page(page_num)
    totalpage = productData1.paginator.num_pages

    data = {
        'productData':productData1,
        'totalpages':[n+1 for n in range(totalpage)]
    }
    return render(request, 'shop.html', data)


def productSingle(request,product_id):
    productDetails = Products.objects.get(id = product_id)
    productData = Products.objects.all()
    # for p in productData:
    #     print(p.product_title)
    data = {
        'productDetails':productDetails,
        'productData':productData,
    }
    return render(request, 'product-single.html',data)


def add_to_cart(request, product_id):
    product = get_object_or_404(Products, pk=product_id)

    if request.user.is_authenticated:
        # User is logged in, add the item to the user's cart
        user_cart_items = CartItem.objects.filter(user=request.user)
        if user_cart_items.count() >= 10:
            messages.error(request, 'You have reached the maximum limit of items in your cart. Please proceed to checkout or remove some items.')
        else:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()
    else:
        # User is not logged in, handle the cart using sessions
        cart = request.session.get('cart', {})
        product_id = str(product_id)
        cart_item = cart.get(product_id)
        if cart_item:
            cart_item['quantity'] += 1
        else:
            cart_item = {'quantity': 1, 'product_id': product_id}
        cart[product_id] = cart_item
        request.session['cart'] = cart

    return redirect('view_cart')


def view_cart(request):
    if request.user.is_authenticated:
        # User is logged in, fetch cart items for the logged-in user
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        # User is not logged in, handle the cart using sessions
        cart = request.session.get('cart', {})
        cart_items = []

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
    
    # Initialize cart_subtotal as a Decimal with value 0.0
    cart_subtotal = 0.0

    for item in cart_items:
        try:
            if isinstance(item, dict):
                # Handle the case for non-logged-in users (item is a dictionary)
                price = item.get('product_price', '0.00').split()
                quantity = item.get('quantity', 1)
            else:
                # Handle the case for logged-in users (item is a CartItem object)
                price = item.product.product_price.split()
                quantity = item.quantity


                for p in price:
                    price_values = float(p.replace('$', ''))
                    product_total = price_values * quantity
                    # Add the product total to the cart_subtotal
                    cart_subtotal += product_total
        except ValueError:
                # Handle cases where product_price is not a valid number
                price = 0.0

    cart_total = cart_subtotal  # You can apply discounts or shipping costs here if needed
    cartdata = {'cart_items': cart_items, 'cart_subtotal': cart_subtotal, 'cart_total': cart_total, 'cart_count': cart_count}
    
    return render(request, 'cart.html', cartdata)


# def update_quantity(request, cart_item_id):
#     # Get the CartItem object based on the cart_item_id
#     cart_item = get_object_or_404(CartItem, pk=cart_item_id)

#     if request.method == 'GET':
#         try:
#             new_quantity = int(request.GET.get('value', 1))  # Use request.GET for query parameters
#             if new_quantity > 0:
#                 cart_item.quantity = new_quantity
#                 cart_item.save()            
#                 return redirect('index')
#             else:          
#                 return redirect('view_cart')
#         except ValueError:
#             return redirect('view_cart')
#     return redirect('view_cart')


def remove_from_cart(request, cart_item_id):
    if request.user.is_authenticated:
        # User is logged in, delete the cart item for the logged-in user
        cart_item = get_object_or_404(CartItem, pk=cart_item_id, user=request.user)
        cart_item.delete()
    else:
        # User is not logged in, handle the cart using sessions
        cart = request.session.get('cart', {})
        if cart_item_id in cart:
            del cart[cart_item_id]
            request.session['cart'] = cart

    return redirect('view_cart')

@login_required
def checkout(request, cartdata):
    cart_items = cartdata['cart_items']
    cart_subtotal = cartdata['cart_subtotal']
    cart_total = cartdata['cart_total']
    cart_count = cartdata['cart_count']

    checkoutdata = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'cart_total': cart_total,
        'cart_count': cart_count,
    }

    return render(request, 'checkout.html', checkoutdata)


def about(request):
    return render(request, 'about.html')


def blog(request):
    blogData = Blogs.objects.all()
    data = {'blogData':blogData,}
    return render(request, 'blog.html',data)

def blogSingle(request,blog_id):
    blogDetails = Blogs.objects.get(id = blog_id)
    blogData = Blogs.objects.all()
    data = {
        'blogDetails':blogDetails,
        'blogData':blogData,
    }
    return render(request, 'blog-single.html',data)


def contact(request):
    return render(request, 'contact.html')

def process_order(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user

            # Get the cart items for the logged-in user
            cart_items = CartItem.objects.filter(user=user)

            if not cart_items.exists():
                messages.error(request, 'Your cart is empty.')
                return redirect('view_cart')

            total = Decimal(0.0)

            # Calculate the total cost of the order
            with transaction.atomic():
                order = Order.objects.create(user=user, total=total)

                for cart_item in cart_items:
                    product = cart_item.product
                    quantity = cart_item.quantity

                    # Create an OrderDetail instance for each product in the cart
                    OrderDetail.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        subtotal=product.product_price * quantity
                    )

                    # Update the inventory or stock of the product if needed
                    product.inventory -= quantity
                    product.save()

                    # Update the total cost of the order
                    total += product.product_price * quantity

                order.total = total
                order.save()

            # Clear the user's cart after order processing
            cart_items.delete()

            messages.success(request, 'Your order has been successfully processed.')
            return redirect('order_confirmation', order.id)

        else:
            messages.error(request, 'You need to log in to place an order.')
            return redirect('login')

    else:
        # Handle cases where users try to access the processing without a POST request
        return redirect('view_cart')



