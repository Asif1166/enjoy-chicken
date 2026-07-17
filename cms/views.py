from django.shortcuts import redirect, render
from django.urls import reverse
from datetime import datetime, timedelta
from cms.forms import ContactForm
from cms.models import *
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django.http import JsonResponse
from io import BytesIO
import logging
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.shortcuts import render, get_object_or_404
from shop.models import CartOrder, CostSettings, Product, SuperCategory
# Create your views here.



def about(request):
    about_us = AboutSection.objects.first()
    counters = Counter.objects.all()
    team_members = TeamMember.objects.all()
    services = Service.objects.all()
    feedbacks = Feedback.objects.all()

    about_section_body = AboutSectionBody.objects.first()
    checklist_items = about_section_body.checklist.split(',') if about_section else []
    
    context = {
        'about_us': about_us,
        'counters': counters,
        'team_members': team_members,
        'services': services,
        'feedbacks': feedbacks,
        'about_section_body': about_section_body,
        'checklist_items': checklist_items,
    }
    return render(request, 'cms/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'cms/contact.html', context)

def photo_gallery(request):
    photo_galleries = PhotoGallery.objects.all().order_by('position')
    context = {
        'photo_galleries': photo_galleries,
    }
    return render(request, 'cms/photo_gallery.html', context)

def video_gallery(request):
    video_galleries = VideoGallery.objects.all().order_by('position')
    context = {
        'video_galleries': video_galleries,
    }
    return render(request, 'cms/video_gallery.html', context)


def generate_reservation_pdf_html(reservation):
    """Generate PDF from HTML template for reservation using xhtml2pdf."""
    
    # Define context data to render the HTML template
    context = {
        'reservation_code': f"#{reservation.id:05d}",
        'submitted_time': datetime.now().strftime('%H:%M %a, %d %b %Y'),
    }
    
    # Render the HTML template with the context data
    html_content = render_to_string("reservation_code_template.html", context)
    
    # Convert HTML to PDF using xhtml2pdf
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    
    # Check for errors
    if pisa_status.err:
        raise Exception("Error generating PDF")
    
    # Return PDF buffer
    pdf_file.seek(0)
    return pdf_file


def save_pdf_to_invoice_slip(reservation):
    """Generate PDF and save it directly to the reservation's invoice_slip field."""
    try:
        pdf_buffer = generate_reservation_pdf_html(reservation)  # Generate PDF
        pdf_file_name = f"reservation_{reservation.id:05d}_invoice.pdf"
        reservation.invoice_slip.save(pdf_file_name, ContentFile(pdf_buffer.getvalue()), save=True)
    except Exception as e:
        logger.error(f"Error saving PDF to invoice_slip: {e}")



def check_slot_availability(date, slot, requested_persons):
    """Helper function to check slot availability"""
    # Check if it's Friday and the slot is one of the lunch hours
    friday_closed_slots = ["11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00"]
    if date.weekday() == 4 and slot in friday_closed_slots:  # Friday is weekday 4 (Monday is 0)
        return 0, 20  # Return as fully booked
    
    booked_seats = Reservation.objects.filter(
        date=date,
        slot=slot,
        status='Réservé'
    ).aggregate(
        total=Sum('total_person')
    )['total'] or 0
    
    available_seats = 20 - booked_seats
    return available_seats, booked_seats

logger = logging.getLogger(__name__)



import json
from decimal import Decimal
from django.conf import settings
import stripe
from shop.models import *

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_menu_api(request):
    categories = Category.objects.all()
    data = []
    for cat in categories:
        products = Product.objects.filter(category=cat, status=True)
        product_data = []
        for p in products:
            product_data.append({
                'id': p.id,
                'title': p.title,
                'price': float(p.price) if p.price else 0,
                'image': p.image.url if p.image else '',
            })
        if product_data:
            data.append({
                'category': cat.title,
                'products': product_data
            })
    return JsonResponse({'menu': data})

def reservation(request):
    site_settiings = SiteSettings.objects.last()
    reservation = Reservation.objects.all().order_by("-id")[:6]

    error_message = None
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        slot = request.POST.get('slot')
        total_person = int(request.POST.get('total_person'))
        
        # Order Data from frontend (JSON string)
        order_items_json = request.POST.get('order_items')
        
        # Determine Payment Method
        payment_method = request.POST.get('payment_method', 'pay_on_spot')


        # Convert date string to date object
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            try:
                date_obj = datetime.strptime(date, '%m/%d/%Y').date()
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': "Invalid date format. Please use YYYY-MM-DD or MM/DD/YYYY format."
                })
        
        # Check if the selected date is a Friday and the slot is one of the lunch hours
        friday_closed_slots = ["11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00"]
        if date_obj.weekday() == 4 and slot in friday_closed_slots:
            return JsonResponse({
                'status': 'error',
                'message': "Sorry, we are closed for lunch hours on Fridays. Please select an evening slot or another day."
            })
       
        available_seats, booked_seats = check_slot_availability(date_obj, slot, total_person)

        if available_seats <= 0:
            return JsonResponse({
                'status': 'error',
                'message': f"Sorry, the slot {slot} on {date} is fully booked. Please try another slot."
            })
        elif total_person > available_seats:
            return JsonResponse({
                'status': 'error',
                'message': f"Sorry, only {available_seats} seats are available for slot {slot} on {date}. Please reduce the number of persons or try another slot."
            })
        
        try:
            # 1. Create Reservation
            data = Reservation(
                name=name, 
                email=email, 
                phone=phone,
                date=date_obj, 
                slot=slot, 
                total_person=total_person,
                status='En attente'  # Default to Pending
            )
            data.save()
            
            # invoice generation moved to success view

            # 2. Process Order 
            payment_url = None
            if order_items_json:
                order_items = json.loads(order_items_json)
                
                if order_items:
                    total_amount = 0
                    
                    # Create CartOrder
                    order = CartOrder.objects.create(
                        user=request.user if request.user.is_authenticated else None,
                        price=0, 
                        total_cost=0, 
                        payment_method="Stripe",
                        order_type="dine_in", 
                        processed=False,
                        paid_status=False
                    )
                    
                    # Create Order Items
                    for item in order_items:
                        product = Product.objects.get(id=item['id'])
                        qty = int(item['qty'])
                        price = Decimal(item['price'])
                        total = price * qty
                        total_amount += float(total)
                        
                        CartOrderItems.objects.create(
                            order=order,
                            product=product,
                            invoice_no="RES-" + str(data.id),
                            item=product.title,
                            image=product.image.url if product.image else '',
                            qty=qty,
                            price=price,
                            total=total
                        )

                    # Update Order Totals
                    cost_settings = CostSettings.objects.last()
                    tax_rate = cost_settings.tax_rate if cost_settings else 0
                    tax_amount = (Decimal(total_amount) * Decimal(tax_rate) / Decimal(100)).quantize(Decimal('0.01'))
                    
                    order.price = total_amount
                    order.tax_amount = tax_amount
                    order.total_cost = Decimal(total_amount) + tax_amount
                    order.save()
                    
                    # Link Order to Reservation
                    data.order = order
                    data.save()
                    
                    # ALWAYS Initiate Stripe Payment
                    try:
                        success_url = request.build_absolute_uri(reverse('reservation_success')) + '?session_id={CHECKOUT_SESSION_ID}'
                        cancel_url = request.build_absolute_uri(reverse('reservation'))
                        
                        checkout_session = stripe.checkout.Session.create(
                            payment_method_types=['card'],
                            line_items=[{
                                'price_data': {
                                    'currency': 'eur',
                                    'product_data': {
                                        'name': f'Reservation #{data.id} - {name}',
                                    },
                                    'unit_amount': int(order.total_cost * 100),
                                },
                                'quantity': 1,
                            }],
                            mode='payment',
                            success_url=success_url,
                            cancel_url=cancel_url,
                        )
                        payment_url = checkout_session.url
                        order.stripe_session_id = checkout_session.id
                        order.save()

                    except Exception as e:
                        print(e)
                        return JsonResponse({'status': 'error', 'message': 'Payment initiation failed.'})
                else:
                     return JsonResponse({'status': 'error', 'message': 'Please select at least one item from the menu.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Menu selection is mandatory.'})


            return JsonResponse({
                'status': 'success',
                'message': 'Redirecting to payment...',
                'payment_url': payment_url
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred while saving your reservation. Please try again.'
            })

    # Get next 7 days dates
    dates = []
    today = timezone.now().date()
    for i in range(7):
        dates.append(today + timedelta(days=i))

    # Get all slots
    slots = [slot[0] for slot in SLOT]

    # Calculate availability for each date and slot
    availability_data = []
    for current_date in dates:
        slot_data = []
        
        is_friday = current_date.weekday() == 4  # Check if the day is Friday
        friday_closed_slots = ["11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00"]
        
        for slot in slots:
            # If it's Friday and the slot is one of the lunch hours, mark as unavailable
            if is_friday and slot in friday_closed_slots:
                available_seats = 0
                badge_class = 'badge-danger'
            else:
                available_seats, _ = check_slot_availability(current_date, slot, 0)
                
                # Determine badge class based on availability
                if available_seats <= 0:
                    badge_class = 'badge-danger'
                elif available_seats < 20:
                    badge_class = 'badge-warning'
                else:
                    badge_class = 'badge-success'
                
            slot_data.append({
                'time': slot,
                'available': 0 if (is_friday and slot in friday_closed_slots) else available_seats,
                'badge_class': badge_class
            })
            
        availability_data.append({
            'date': current_date,
            'day_name': current_date.strftime('%A'),
            'slots': slot_data
        })

    context = {
        'availability_data': availability_data,
        'reservation': reservation,
        'error_message': error_message,
        'site_settiings': site_settiings,
        'is_reservation': site_settiings.is_reservation if site_settiings.is_reservation else False,
    }
    return render(request, 'cms/reservation.html', context)




def product(request):




    super_categories = SuperCategory.objects.all().prefetch_related('category_set__product_set')
    products = Product.objects.all()

    

    context = {
 
        'super_categories': super_categories,
        'products': products,
      
    }
    
    return render(request, 'cms/product.html', context)


def track_order(request):
    order_id = request.GET.get('order_id', None)
    phone_no = request.GET.get('phone_no', None)

    order = None
    order_not_found = False
    order_display_id = None

    # Validate that both order_id and phone_no are provided
    if not order_id or not phone_no:
        order_not_found = True
    else:
        try:
            # Query with both order_id and phone_no
            order = CartOrder.objects.select_related('shipping_address').prefetch_related(
                'cartorderitems_set__product'
            ).get(
                id=order_id,
                shipping_address__phone=phone_no
            )
            order_display_id = f"{order.id:05}"  # Format order ID
        except CartOrder.DoesNotExist:
            order_not_found = True

    cost_settings = CostSettings.objects.last()

    context = {
        'order': order,
        'cost_settings': cost_settings,
        'order_not_found': order_not_found,
        'order_display_id': order_display_id,
    }

    return render(request, 'cms/track_order.html', context)



def reservation_success(request):
    session_id = request.GET.get('session_id')
    reservation = None
    invoice_url = None
    
    if session_id:
        try:
             # Verify Stripe Session
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                order = CartOrder.objects.get(stripe_session_id=session_id)
                order.paid_status = True
                order.save()
                
                reservation = Reservation.objects.get(order=order)
                if reservation.status != 'Réservé':
                    reservation.status = 'Réservé'
                    reservation.save()
                    
                    # Generate Invoice now
                    save_pdf_to_invoice_slip(reservation)
                
                invoice_url = f"/media/invoices/reservation_{reservation.id:05d}_invoice.pdf"
            
        except Exception as e:
            print(f"Error validating reservation payment: {e}")
    
    return render(request, 'cms/reservation_success.html', {
        'reservation': reservation,
        'invoice_url': invoice_url
    })
