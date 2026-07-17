from cms.models import *
from .models import *
from shop.models import *

def default(request):
    menus = Menu.objects.all().prefetch_related('submenus').order_by('position')
    categories = Category.objects.all()
    site = SiteSettings.objects.first()
    address = None
    wishlist_count = 0  # Initialize wishlist_count to avoid UnboundLocalError

    if request.user.is_authenticated:
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:
            address = None

    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        print('wishlist_count', wishlist_count)

    site_info = SiteInfo.objects.first()

    return {
        'categories': categories,
        'address': address,
        'menus': menus,
        'site': site,
        'wishlist_count': wishlist_count,
        'site_info': site_info,
    }