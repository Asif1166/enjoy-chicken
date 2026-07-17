from django.shortcuts import render
import stripe
from django.conf import settings
from cms.models import SiteSettings
from cms.models import Reservation
from shop.forms import CostSettingsForm, DateRangeForm
from shop.models import CartOrder, CostSettings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shop.utils import generate_invoice_pdf, generate_pdf_report
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.


def superuser_required(function):
    """Decorator to check if the user is a superuser."""
    def _inner(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            # Redirect or show an error if the user is not a superuser
            return redirect('admin_login')  # Replace 'home' with the URL name for the home page or error page
    return _inner


@superuser_required
def admin_dashboard(request):

    context = {
       

    }
    
    return render(request, 'custom_admin/home/custom_admin_home.html', context)



@superuser_required
def orders(request):
    site_settings = SiteSettings.objects.last()

    cart_orders = CartOrder.objects.all().select_related(
        'shipping_address'
    ).prefetch_related(
        'cartorderitems_set__product'
    ).order_by('-id')

    paginator = Paginator(cart_orders, 15)
    page = request.GET.get('page')

    try:
        cart_orders = paginator.page(page)
    except PageNotAnInteger:
        cart_orders = paginator.page(1)
    except EmptyPage:
        cart_orders = paginator.page(paginator.num_pages)

    form = DateRangeForm(request.GET or None)

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if 'generate_pdf' in request.GET:
            return generate_pdf_report(start_date, end_date)

    # Handle CostSettings form
    cost_settings = CostSettings.objects.last()
    cost_form = CostSettingsForm(request.POST or None, instance=cost_settings)

    if request.method == 'POST' and cost_form.is_valid():
        cost_form.save()
        messages.success(request, "Shipping cost updated successfully!")
        return redirect('orders')

    context = {
        'cart_orders': cart_orders,
        'form': form,
        'cost_form': cost_form,
        'cost_settings': cost_settings,
        'site_settings': site_settings,
    }

    return render(request, 'custom_admin/orders/orders.html', context)


@require_POST
@superuser_required
def toggle_take_away_on_off_status(request):
    site_settings = SiteSettings.objects.last()
    if site_settings:
        site_settings.is_take_away_enabled = not site_settings.is_take_away_enabled
        site_settings.save()
        return JsonResponse({'status': 'success', 'is_take_away_enabled': site_settings.is_take_away_enabled})
    return JsonResponse({'status': 'error', 'message': 'Failed to update delivery status'})


@require_POST
@superuser_required
def toggle_delivery_on_off_status(request):
    site_settings = SiteSettings.objects.last()
    if site_settings:
        site_settings.is_delivery_enabled = not site_settings.is_delivery_enabled
        site_settings.save()
        return JsonResponse({'status': 'success', 'is_delivery_enabled': site_settings.is_delivery_enabled})
    return JsonResponse({'status': 'error', 'message': 'Failed to update delivery status'})


@require_POST
@superuser_required
def toggle_order_on_off_status(request):
    site_settings = SiteSettings.objects.last()
    if site_settings:
        site_settings.is_order = not site_settings.is_order
        site_settings.save()
        return JsonResponse({'status': 'success', 'is_order': site_settings.is_order})
    return JsonResponse({'status': 'error', 'message': 'Failed to update order status'})

def toggle_paid_status(request, order_id):
    order = get_object_or_404(CartOrder, id=order_id)
    order.paid_status = not order.paid_status  # Toggle the paid status
    order.save()
    
    # Display a success message
    if order.paid_status:
        messages.success(request, "Order marked as Paid.")
    else:
        messages.success(request, "Order marked as Due.")
    
    return redirect('orders')


@csrf_exempt
def update_order_status(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('product_status')

        try:
            order = CartOrder.objects.get(id=order_id)
            order.product_status = new_status

            # Check if the new status is "canceled" and payment method is "Stripe"
            if new_status == "canceled" and order.payment_method == "Stripe":
                # Assuming you saved Stripe's payment intent ID with the order, named `stripe_payment_intent_id`
                if order.stripe_payment_intent_id:
                    try:
                        # Process a refund
                        refund = stripe.Refund.create(
                            payment_intent=order.stripe_payment_intent_id,
                        )
                        order.save()  # Save the order after refund
                        return JsonResponse({'status': 'success', 'message': 'Order status updated and refund processed.'})
                    except stripe.error.StripeError as e:
                        # Handle any errors from Stripe
                        return JsonResponse({'status': 'error', 'message': 'Refund failed: ' + str(e)}, status=500)
                else:
                    return JsonResponse({'status': 'error', 'message': 'No Stripe payment intent ID found for this order.'}, status=400)
            else:
                # Just save the new status if no refund is needed
                order.save()
                return JsonResponse({'status': 'success', 'message': 'Order status updated.'})

        except CartOrder.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def download_invoice(request, order_id):
    return generate_invoice_pdf(order_id)


def delete_sale(request, order_id):
    # Handle the request with both GET and POST
    if request.method == 'GET':  # Handle the deletion directly via GET
        try:
            order = get_object_or_404(CartOrder, id=order_id)
            order.delete()
            # Redirect after deletion to a success page or the orders list
            return redirect('orders')  # Replace 'orders_list' with your desired redirect URL
        except Exception as e:
            # Handle any exceptions, perhaps logging them or redirecting with an error message
            return redirect('orders')  # Replace with an error page if desired
    return redirect('orders')  # Fallback redirect if the method is not GET




def report_view(request):
    form = DateRangeForm(request.GET or None)

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if 'generate_pdf' in request.GET:
            return generate_pdf_report(start_date, end_date)

    return render(request, 'custom_admin/orders/reports.html', {'form': form})



def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Check if the user is a superuser
            if user.is_superuser:
                login(request, user)
                return redirect('orders')  # Redirect to admin dashboard or another page
            else:
                messages.error(request, 'You must be a superuser to access this panel.')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'custom_admin/signin.html')


def admin_logout(request):
    logout(request) 
    return redirect('admin_login')


def process_all_orders(request):
    if request.method == 'POST':
        CartOrder.objects.filter(processed=False).update(processed=True)
        return redirect('orders')


def fetch_orders_data(request):
    # Filter CartOrder with the specified conditions
    cart_orders = CartOrder.objects.select_related('shipping_address', 'user').filter(
        Q(payment_method='Stripe', paid_status=True) | Q(~Q(payment_method='Stripe'), paid_status=False),
        processed=False
    ).order_by('-id')
    
    # Prepare data for JSON response
    orders_data = []
    for order in cart_orders:
        orders_data.append({
            'id': order.id,
            'customer_name': order.shipping_address.name if order.shipping_address else '',
            'customer_email': order.shipping_address.email if order.shipping_address else '',
            'customer_phone': order.shipping_address.phone if order.shipping_address else '',
            'customer_street_address': order.shipping_address.street_address if order.shipping_address else '',
            'customer_zip_code': order.shipping_address.zip_code if order.shipping_address else '',
            'customer_city': order.shipping_address.city if order.shipping_address else '',
            'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'price': order.price,
            'payment_method': order.payment_method,
            'product_status': order.product_status,
            'paid_status': order.paid_status,
            'order_type': order.order_type,
            'stripe_payment_intent_id': order.stripe_payment_intent_id,
            'shipping_cost': order.shipping_cost,
            'payment_icon': '/static/custom_admin_css/assets/img/icons/stripe.svg' if order.payment_method == 'Stripe' else None,
        })

    return JsonResponse({'orders': orders_data})



@superuser_required
def reservation_list(request):
    # Fetch all CartOrders with related CartOrderItems, Products, and ShippingAddress
    reservations = Reservation.objects.all().order_by('-id')
    site_settings =SiteSettings.objects.last()

    # Paginate the cart_orders queryset
    paginator = Paginator(reservations, 15)  # 30 orders per page
    page = request.GET.get('page')
    
    try:
        reservations = paginator.page(page)
    except PageNotAnInteger:
        reservations = paginator.page(1)
    except EmptyPage:
        reservations = paginator.page(paginator.num_pages)


    
    context = {
        'reservations': reservations,
        'site_settings': site_settings,
       
    }
    
    return render(request, 'custom_admin/reservation/reservation_list.html', context)

@require_POST
@superuser_required
def toggle_reservation_status(request):
    site_settings = SiteSettings.objects.last()
    if site_settings:
        site_settings.is_reservation = not site_settings.is_reservation
        site_settings.save()
        return JsonResponse({'status': 'success', 'is_reservation': site_settings.is_reservation})
    return JsonResponse({'status': 'error', 'message': 'Failed to update reservation status'})


def delete_reservation(request, reservation_id):
    if request.method == 'GET': 
        try:
            reservation = get_object_or_404(Reservation, id=reservation_id)
            reservation.delete()

            return redirect('reservation_list')
        except Exception as e:
           
            return redirect('reservation_list')
    return redirect('reservation_list') 


@csrf_exempt
def update_reservation_status(request):
    if request.method == "POST":
        reservation_id = request.POST.get('reservation_id')
        new_status = request.POST.get('status')

        print(f'Order ID: {reservation_id}, New Status: {new_status}')

        try:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.status = new_status
            reservation.save()
            return JsonResponse({'status': 'success'})
        except Reservation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Reservation not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)