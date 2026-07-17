import tempfile
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum, Avg
from cms.models import SiteSettings
from shop.forms import ProductReviewForm
from shop.models import *
from django.template.loader import render_to_string
from authentication.models import *
from django.db.models import Sum
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.db.models import Q
from io import BytesIO
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404
from .models import CartOrder, CartOrderItems
from xhtml2pdf import pisa
import tempfile
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
import stripe

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
def product_list_view(request):
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 2000)
    categories = request.GET.getlist('categories')
    statuses = request.GET.getlist('statuses')

    # Queryset for products
    products = Product.objects.all()

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if categories:
        products = products.filter(category__id__in=categories)  # Ensure filtering by category ID
    if statuses:
        products = products.filter(product_status__in=statuses)

    # Pass all filter options to template
    context = {
        'products': products,
        'categories': Category.objects.all(),  # Fetch all categories
        'selected_categories': categories,     # Pass selected categories to template
        'selected_statuses': statuses,         # Pass selected statuses to template
        'min_price': min_price,
        'max_price': max_price,
    }
    
    return render(request, 'shop/product.html', context)

def category_list_view(request):
    
    categories = Category.objects.all()
    products = Product.objects.all()
    
    context = {
        'categories': categories,
        'products': products,
    }
    
    return render(request, 'shop/category.html', context)

def category_product_list_view(request, cid):
    category = get_object_or_404(Category, cid=cid)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
        'categories': Category.objects.all(), 
    }

    return render(request, 'shop/product.html', context)


def super_category_product_list_view(request):
    # Retrieve all super categories and their associated categories and products
    super_category_products = []
    super_categories = SuperCategory.objects.all()
    print('super_categories', super_categories)
    
    for super_category in super_categories:
        category_products = []
        categories = Category.objects.filter(super_category=super_category)
        
        for category in categories:
            products = Product.objects.filter(category=category)
            category_products.append({
                'category': category,
                'products': products
            })
        
        super_category_products.append({
            'super_category': super_category,
            'category_products': category_products
        })

    context = {
        'super_category_products': super_category_products,
    }

    return render(request, 'shop/product.html', context)



def product_details_view(request, pid):
    product = Product.objects.get(pid=pid)
    p_images = product.p_images.all()
    
    related_products = Product.objects.filter(category=product.category).exclude(pid=pid)[:6]
    review = ProductReview.objects.filter(product=product).order_by('-date')
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    site_settiings = SiteSettings.objects.last()
    
    # Prepare the data to be sent as JSON

    # Handle form submission
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            if request.user.is_authenticated:
                review.user = request.user
            review.save()
            return redirect('product_details', pid=pid)
    else:
        form = ProductReviewForm()

    context = {
        'product': product,
        'p_images': p_images,
        'related_products': related_products,
        'review': review,
        'average_rating': average_rating,
        'form': form,
        'site_settiings': site_settiings,
        'is_order': site_settiings.is_order if site_settiings else False,
    }
    
    return render(request, 'shop/product_details.html', context)


def search_view(request):
    query = request.GET.get("q")
    
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(category__title__icontains=query)
        ).order_by("-date")
    else:
        products = Product.objects.none()  # Return an empty queryset if there's no query
    
    context = {
        'products': products,
        'query': query,
    }
    
    return render(request, 'shop/search.html', context)


    
    
def get_cart(request):
    if request.user.is_authenticated:
        # Get or create cart for authenticated users
        cart, created = CartOrder.objects.get_or_create(user=request.user)
    else:
        # Use session key for anonymous users
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = CartOrder.objects.get_or_create(session_key=session_key)
    return cart

# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart = get_cart(request)
    
#     cart_item, created = CartOrderItems.objects.get_or_create(order=cart, product=product)
    
#     if not created:
#         cart_item.qty += 1
#         cart_item.save()

#     return redirect('cart_view')


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'pid': request.GET['pid'],
        # Only add 'image' if it's not an empty string
        'image': request.GET.get('image', ''),
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})




def view_cart(request):
    cart_total_amount = 0
    cart_data = request.session.get('cart_data_obj', {})


    if cart_data:
        for p_id, item in cart_data.items():
            # Ensure that the price and total values are valid and calculable
            try:
                quantity = int(item['qty'])
                price = float(item['price'])
                item['total'] = quantity * price
                cart_total_amount += item['total']
            except (ValueError, KeyError) as e:
                print(f"Error processing item with product ID {p_id}: {e}")
                continue

        return render(request, 'shop/cart.html', {
            "cart_data": cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount
        })
    else:
        return render(request, 'shop/cart.html', {
            "cart_data": "",
            'totalcartitems': 0,
            'cart_total_amount': cart_total_amount
        })
    




def add_to_wishlist(request):
    # Extracting product data from the request
    product_id = str(request.GET['id'])
    product_title = request.GET['title']
    product_pid = request.GET['pid']
    product_image = request.GET['image']

    # Store in session
    wishlist_product = {
        product_id: {
            'title': product_title,
            'pid': product_pid,
            'image': product_image,
        }
    }

    # Check if wishlist_data_obj exists in the session
    if 'wishlist_data_obj' in request.session:
        if product_id in request.session['wishlist_data_obj']:
            # If the product is already in the session-based wishlist, do nothing or update it
            wishlist_data = request.session['wishlist_data_obj']
            wishlist_data.update(wishlist_data)
            request.session['wishlist_data_obj'] = wishlist_data
        else:
            wishlist_data = request.session['wishlist_data_obj']
            wishlist_data.update(wishlist_product)
            request.session['wishlist_data_obj'] = wishlist_data
    else:
        request.session['wishlist_data_obj'] = wishlist_product

    # Save to database for authenticated users
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
        )

    if request.user.is_authenticated:
        # Fetch updated wishlist count
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    # Return JSON response with the wishlist data and total count
    return JsonResponse({"data": request.session['wishlist_data_obj'], 'totalwishlistitems': wishlist_count})

def view_wishlist(request):
    if request.user.is_authenticated:
        # Fetch the wishlist for the logged-in user
        wishlist_items = Wishlist.objects.filter(user=request.user)
        
        # Extract products from the wishlist items
        products = [item.product for item in wishlist_items]
    else:
        # Handle the case for unauthenticated users
        products = []

    context = {
        'products': products
    }
    return render(request, 'shop/wishlist.html', context)


    

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    
    # Initialize cart total amount
    cart_total_amount = 0
    
    # Retrieve the cart data from the session
    cart_data = request.session.get('cart_data_obj', {})

    # Check if the product exists in the cart and delete it
    if product_id in cart_data:
        del cart_data[product_id]
        request.session['cart_data_obj'] = cart_data

    # Recalculate the cart total amount and update item totals
    for p_id, item in cart_data.items():
        price = item.get('price', '').strip()
        if price:
            try:
                item['total'] = int(item['qty']) * float(price)
                cart_total_amount += item['total']
            except ValueError:
                item['total'] = 0.0  # Default to 0 if price is invalid
                cart_total_amount += item['total']
    
    # Render the updated cart template as a string
    context = render_to_string(
        "shop/async/cart-list.html", 
        {
            "cart_data": cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount
        }
    )
    
    # Return the updated cart data and totals as JSON response
    return JsonResponse({
        "data": context, 
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount  # Send the total cart amount to update subtotal
    })


def delete_item_from_wishlist(request):
    product_id = str(request.GET.get('id'))

    # Initialize the total wishlist amount
    wishlist_total_amount = 0

    if request.user.is_authenticated:
        # Debugging: Check what product_id is received
        print(f"Received product_id: {product_id}")

        # Delete the wishlist item from the database
        deleted_count, _ = Wishlist.objects.filter(user=request.user, product_id=product_id).delete()

        # Debugging: Check if any items were deleted
        print(f"Number of deleted items: {deleted_count}")

        # Retrieve updated wishlist data
        wishlist = Wishlist.objects.filter(user=request.user)

        # Recalculate the wishlist total amount and update item totals
        wishlist_data = {}
        for item in wishlist:
            product = item.product
            wishlist_data[product.id] = {
                'title': product.title,
                'image': product.image.url if product.image else '',
                'price': float(product.price),
                'quantity': 1  # Assuming each item in wishlist is single quantity
            }
            wishlist_total_amount += float(product.price)

        # Render the updated wishlist template as a string
        context = render_to_string(
            "shop/async/wishlist-list.html",
            {
                "wishlist_data": wishlist_data,
                'totalwishlistitems': len(wishlist_data),
                'wishlist_total_amount': wishlist_total_amount
            }
        )

        # Return the updated wishlist data and totals as JSON response
        return JsonResponse({
            "data": context,
            'totalwishlistitems': len(wishlist_data),
            'wishlist_total_amount': wishlist_total_amount
        })
    else:
        return JsonResponse({"error": "User not authenticated"}, status=403)


def update_form_cart(request):
    
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    
    
    # Initialize cart total amount
    cart_total_amount = 0
    
    # Retrieve the cart data from the session
    cart_data = request.session.get('cart_data_obj', {})

    # Check if the product exists in the cart and delete it
    if product_id in cart_data:
        cart_data[str(request.GET['id'])]['qty'] = product_qty
        request.session['cart_data_obj'] = cart_data

    # Recalculate the cart total amount and update item totals
    for p_id, item in cart_data.items():
        price = item.get('price', '').strip()
        if price:
            try:
                item['total'] = int(item['qty']) * float(price)
                cart_total_amount += item['total']
            except ValueError:
                item['total'] = 0.0  # Default to 0 if price is invalid
                cart_total_amount += item['total']
    
    # Render the updated cart template as a string
    context = render_to_string(
        "shop/async/cart-list.html", 
        {
            "cart_data": cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount
        }
    )
    
    # Return the updated cart data and totals as JSON response
    return JsonResponse({
        "data": context, 
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount  # Send the total cart amount to update subtotal
    })


def checkout_view(request):
    site_settiings = SiteSettings.objects.last()

    cart_total_amount = 0
    
    if "cart_data_obj" in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    cost_settings = CostSettings.objects.last()

    if cost_settings:
        # Calculate tax and shipping based on cost settings
        shipping_cost = cost_settings.shipping_cost
        tax_rate = cost_settings.tax_rate
        tax_amount = (Decimal(cart_total_amount) * Decimal(tax_rate) / Decimal(100)).quantize(Decimal('0.00'))
        print('tax_amount', tax_amount)

        total_cost = Decimal(cart_total_amount) + shipping_cost
    else:
        shipping_cost = Decimal('0.00')
        tax_amount = Decimal('0.00')

        total_cost = Decimal(cart_total_amount)

    # Calculate remaining amount needed for minimum order (30 euros)
    minimum_order_amount = Decimal('30.00')
    remaining_amount = Decimal('0.00')
    if cart_total_amount < minimum_order_amount:
        remaining_amount = minimum_order_amount - Decimal(cart_total_amount)
    
    context = {
        "cart_data": request.session.get('cart_data_obj', {}),
        "totalcartitems": len(request.session.get('cart_data_obj', {})),
        "cart_total_amount": Decimal(cart_total_amount),
        "shipping_cost": shipping_cost,
        "total_cost": total_cost,
        "cost_settings": cost_settings,
        "tax_amount": tax_amount if tax_amount else Decimal('0.00'),
        'is_delivery_enabled': site_settiings.is_delivery_enabled,
        'is_take_away_enabled': site_settiings.is_take_away_enabled,
        'remaining_amount': remaining_amount,  # Amount needed to reach 30 euros
        'minimum_order_amount': minimum_order_amount,
    }        
    return render(request, 'shop/checkout.html', context)


def order_complete_view(request):
    cart_total_amount = 0
    total_amount = 0

    if request.method == "POST":
        # Process shipping address form data
        shipping_address = ShippingAddress.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=request.POST.get('email'),
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            country=request.POST.get('country'),
            street_address=request.POST.get('street'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip'),
            order_notes=request.POST.get('ordernotes'),
        )
        
        # Calculate total amount
        for p_id, item in request.session.get('cart_data_obj', {}).items():
            total_amount += int(item['qty']) * float(item['price'])
        

        # Fetch latest cost settings for shipping and tax
        cost_settings = CostSettings.objects.last()
        if cost_settings:
            shipping_cost = cost_settings.shipping_cost


            tax_rate = cost_settings.tax_rate
            tax_amount = (Decimal(total_amount) * Decimal(tax_rate) / Decimal(100)).quantize(Decimal('0.01'))
            print('tax_amountssss', tax_amount)

            total_cost = Decimal(total_amount) + shipping_cost
        else:
            # Default to base amount if no cost settings are found
            shipping_cost = Decimal('0.00')
            tax_amount = Decimal('0.00')
            total_cost = Decimal(total_amount)

        # Handle payment method
        payment_method = request.POST.get('payment_method')
        order_type = request.POST.get('order_type')
        # Create the order and include the payment method
        order = CartOrder.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key if not request.user.is_authenticated else None,
            price=total_amount,
            total_cost=total_cost,
            shipping_address=shipping_address,
            payment_method=payment_method,
            order_type = order_type,
            tax_amount = tax_amount,
            shipping_cost = shipping_cost,
            processed=False
        )

        for p_id, item in request.session.get('cart_data_obj', {}).items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            # Get the product and reduce its quantity
            product = Product.objects.get(pk=p_id)
            product.quantity -= int(item['qty'])
            product.save()

            CartOrderItems.objects.create(
                order=order,
                product=product,
                invoice_no="INVOICE_NO-" + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )
        
        # Clear the cart
        request.session['cart_data_obj'] = {}

        if request.user.is_authenticated:
            Wishlist.objects.filter(user=request.user).delete()

        if payment_method == 'COD':
            # Cash on Delivery: directly redirect to order confirmation
            order.paid_status = False
            order.save()
            return redirect('order_confirmation')
        
        elif payment_method == 'Stripe':
            # Create a Stripe Checkout Session for card payment
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {'name': 'Your Purchase'},
                            'unit_amount': int(total_cost * 100),  # Stripe expects amount in cents
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('order_confirmation')) + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri(reverse('product')),
                )
                
                # Save Stripe session ID for potential refund
                order.stripe_session_id = session.id
                order.save()

                # Redirect to Stripe payment page
                return redirect(session.url, code=303)
            
            except stripe.error.StripeError as e:
                # Handle Stripe error, log it, and notify the user
                print(f"Stripe error: {e.user_message}")
                return JsonResponse({'status': 'error', 'message': e.user_message}, status=500)


    else:
        return render(request, 'shop/order_complete.html', {
            "cart_data": request.session.get('cart_data_obj', {}),
            'totalcartitems': len(request.session.get('cart_data_obj', {})),
            'cart_total_amount': cart_total_amount
        })

        
        
def order_confirmation_view(request):
    if request.user.is_authenticated:
        order = CartOrder.objects.filter(user=request.user, paid_status=False).last()
    else:
        order = CartOrder.objects.filter(session_key=request.session.session_key, paid_status=False).last()

    if not order:
        raise Http404("Order not found")

    # Check for successful Stripe payment
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            # Retrieve the session to get payment intent
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = session.payment_intent

            # Update the order with the payment intent and mark as paid
            order = CartOrder.objects.get(stripe_session_id=session_id)
            order.stripe_payment_intent_id = payment_intent
            order.paid_status = True
            order.processed = False
            order.save()
            
        except CartOrder.DoesNotExist:
            print("Order not found.")
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e.user_message}")
            return JsonResponse({'status': 'error', 'message': e.user_message}, status=500)


    order_items = CartOrderItems.objects.filter(order=order)
    shipping_address = order.shipping_address

    phone_number = shipping_address.phone if shipping_address else None

    cost_settings = CostSettings.objects.last()

    return render(request, 'shop/order_confirmation.html', {
        'order': order,
        'order_items': order_items,
        'shipping_address': shipping_address,
        'cost_settings': cost_settings,
        'phone_number': phone_number,
    })


@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        display_name = request.POST.get('username')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Update User and Profile data
        if request.user.check_password(current_password):
            if new_password == confirm_password and new_password:
                request.user.set_password(new_password)
            request.user.username = display_name
            request.user.email = email
            request.user.save()

            profile.full_name = full_name
            profile.save()
            
            messages.success(request, 'Profile updated successfully')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect current password')
            
    user_info = {
        "username": request.user.username,
        "email": request.user.email,
        "full_name": profile.full_name,
    }
    context = {
        "orders": orders,
        "user_info": user_info,
    }
    return render(request, 'shop/customer/dashboard.html', context)


def order_details(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)
    

    context = {
        "order":order,
        "products":products,
    }
    return render(request, 'shop/customer/order_details.html', context)


def track_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        email = request.POST.get('email')

        try:
            order = CartOrder.objects.get(id=order_id, shipping_address__email=email)
            product_status = order.product_status
            return JsonResponse({'status': 'success', 'product_status': product_status})
        except CartOrder.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No order found with the provided details.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def order_track(request):
    return render(request, 'shop/trackorder.html')



def generate_invoice_pdf(request, order_id):
    if request.user.is_authenticated:
        # Fetch the most recent order for the authenticated user
        order = CartOrder.objects.filter(user=request.user, paid_status=False).last()
    else:
        # Fetch the most recent order for anonymous users
        order = CartOrder.objects.filter(session_key=request.session.session_key, paid_status=False).last()

    if not order:
        raise Http404("Order not found")

    # Fetch the order items associated with the order
    order_items = CartOrderItems.objects.filter(order=order)
    
    # Fetch the shipping address associated with the order
    shipping_address = order.shipping_address

    # Render the HTML template with context data
    html_string = render_to_string('shop/invoice_template.html', {
        'order': order,
        'order_items': order_items,
        'shipping_address': shipping_address,
    })
    
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order_id}.pdf'
    
    # Create PDF from the HTML string using xhtml2pdf
    pisa_status = pisa.CreatePDF(BytesIO(html_string.encode('UTF-8')), dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response



def check_new_orders(request):
    # Get orders that have been completed (paid_status=True) but not yet processed
    new_orders_count = CartOrder.objects.filter(paid_status=True, processed=False).count()
    return JsonResponse({'new_orders': new_orders_count})



def fetch_notifications(request):

    notifications = Notification.objects.all().order_by('-created_at')[:5]  # Fetch the latest 5 notifications
    notification_list = [
        {
            'id': notification.id,
            'title': notification.title,
            'details': notification.details,
            'time': notification.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format the time as needed
            'avatar': notification.avatar.url if notification.avatar else None,  # Handle avatar image
        }
        for notification in notifications
    ]
    return JsonResponse({'notifications': notification_list})



def delete_notification(request, notification_id):
    if request.method == 'DELETE':
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            return JsonResponse({'success': True, 'message': 'Notification deleted.'})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Notification not found.'})
    return JsonResponse({'success': False, 'message': 'Unauthorized or invalid request.'})




@csrf_exempt  # Only if you're not using CSRF tokens; otherwise, remove this
def clear_notifications(request):
    if request.method == 'POST':
        Notification.objects.all().delete()  # Delete all notifications for the user
        return JsonResponse({'success': True, 'message': 'All notifications cleared.'})
    return JsonResponse({'success': False, 'message': 'Unauthorized or invalid request.'})
