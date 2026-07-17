from django.shortcuts import render

from cms.models import *
from shop.models import *
from django.utils.timezone import now
from collections import defaultdict
from .forms import CVForm
from django.contrib import messages



def home(request):
    from collections import defaultdict
    from django.utils.timezone import now

    super_categories = SuperCategory.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    featured_products = Product.objects.filter(featured=True)
    countdown = Countdown.objects.order_by('-created_at').first()
    sliders = Slider.objects.all() 
    
    # Initialize variables to prevent UnboundLocalError
    offer_products = []
    offer_products_by_category = defaultdict(list)
    last_offer_product_ids = []  # Track product IDs with the most recent updated_at for highlighting
    
    # Prepare offer products by category if a valid countdown is available
    if countdown and countdown.target_date > now():
        # Get offer products ordered by updated_at (most recent first), fallback to date if updated_at is None
        offer_products = Product.objects.filter(offer_countdown=countdown).order_by('-updated', '-date')
        
        # Find the most recent updated_at timestamp for highlighting
        if offer_products.exists():
            first_product = offer_products.first()
            # Use updated_at if available, otherwise use date
            most_recent_timestamp = first_product.updated if first_product.updated else first_product.date
            
            # Get IDs of products with the most recent timestamp for highlighting
            if first_product.updated:
                # Products with the same updated_at as the most recent one
                last_offer_product_ids = list(
                    offer_products.filter(updated=most_recent_timestamp).values_list('id', flat=True)
                )
            else:
                # If no updated_at, use date field
                last_offer_product_ids = list(
                    offer_products.filter(date=most_recent_timestamp).values_list('id', flat=True)
                )
        
        # Group products by category and maintain order by updated_at
        for product in offer_products:
            if product.category:
                offer_products_by_category[product.category].append(product)

    super_categories = SuperCategory.objects.all().prefetch_related('category_set__product_set')

    brands = Brand.objects.all()
    about_us = AboutSection.objects.first()
    testimonials = Testimonial.objects.all()
    photo_gallery = PhotoGallery.objects.all()
    chefs = Chef.objects.all()
    opening_hours = OpeningHours.objects.prefetch_related('operating_hours').first()
    
    context = {
        'super_categories': super_categories,
        'categories': categories,
        'products': products,
        'featured_products': featured_products,
        'sliders': sliders,
        'countdown': countdown,
        'offer_products': offer_products,
        'offer_products_by_category': dict(offer_products_by_category),
        'last_offer_product_ids': last_offer_product_ids,  # For highlighting last offer products
        'now': now(),
        'brands': brands,
        'about_us': about_us,
        'photo_gallery': photo_gallery,
        'chefs': chefs,
        'opening_hours': opening_hours,
        'testimonials': testimonials,
    }
    
    return render(request, 'home/home.html', context)



