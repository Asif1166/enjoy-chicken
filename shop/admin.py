from django.contrib import admin
from .forms import DateRangeForm
from django.shortcuts import render
from shop.models import *
from .utils import generate_invoice_pdf, generate_pdf_report
from django.urls import path
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.

class ProductImagesyAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesyAdmin]
    list_display = ['title', 'product_img', 'category', 'price','quantity', 'featured', 'product_status']

class SubCategoryAdmin(admin.TabularInline):
    model = SubCategory
    

        
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryAdmin]
    list_display = ['id', 'title', 'image']
    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'vendor_img']
    
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address']
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'date']
    
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)

admin.site.register(Address, AddressAdmin)


admin.site.register(Countdown)
admin.site.register(SuperCategory)
admin.site.register(Wishlist)
admin.site.register(Notification)
admin.site.register(CostSettings)

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'name', 'phone', 'country', 'street_address', 'city', 'state', 'zip_code', 'order_notes', 'status')
    search_fields = ('email', 'name', 'phone', 'country', 'city', 'state', 'zip_code')

@admin.register(CartOrder)
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user',
                    'items_summary',
                    'total_amount',
                    'phone_number', 
                    'email', 
                    'formatted_shipping_address', 
                    'order_date', 
                    'payment_method', 
                    'paid_status', 
                    'product_status',
                    'download_invoice'
                    )
    list_editable = ('product_status', 'paid_status')
    list_filter = ('paid_status', 'order_date', 'product_status')
    search_fields = ('user__username', 'session_key', 'shipping_address__email')
    readonly_fields = ('total_amount', 'items_summary')

    change_list_template = 'admin/cartorder_changelist.html'  # Custom template for change list




    def download_invoice(self, obj):
        return format_html(
            '<a class="button" href="{}">Download Invoice</a>',
            reverse('admin:download_invoice', args=[obj.id])
        )
    download_invoice.short_description = 'Download Invoice'
    download_invoice.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('download-invoice/<int:order_id>/', self.admin_site.admin_view(self.download_invoice_view), name='download_invoice'),
            path('generate-report/', self.admin_site.admin_view(self.generate_report), name='cartorder_generate_report'),
        ]
        return custom_urls + urls

    def download_invoice_view(self, request, order_id):
        return generate_invoice_pdf(order_id)


    def generate_report(self, request):
        if request.method == 'POST':
            form = DateRangeForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                response = generate_pdf_report(start_date, end_date)
                response['Content-Disposition'] = f'attachment; filename="report_{start_date}_to_{end_date}.pdf"'
                return response
        else:
            form = DateRangeForm()

        context = {
            'form': form,
        }
        return render(request, 'admin/generate_report.html', context)

    def total_amount(self, obj):
        return obj.price
    total_amount.short_description = 'Total Amount'

    def items_summary(self, obj):
        items = CartOrderItems.objects.filter(order=obj)
        summary = ', '.join([f'{item.item}  (qty-{item.qty})' for item in items])
        return summary
    items_summary.short_description = 'Items Summary'

    def phone_number(self, obj):
        if obj.shipping_address:
            address = obj.shipping_address
            return (f"{address.phone}")
        return 'No Phone No'
    phone_number.short_description = 'Phone'
    
    def email(self, obj):
        if obj.shipping_address:
            address = obj.shipping_address
            return (f"{address.email}")
        return 'No Phone No'
    email.short_description = 'Email'
    
    def formatted_shipping_address(self, obj):
        if obj.shipping_address:
            address = obj.shipping_address
            return (f"{address.street_address}, {address.city}, {address.state}")
        return 'No shipping address'
    formatted_shipping_address.short_description = 'Shipping Address'
    
@admin.register(CartOrderItems)
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'invoice_no', 'item', 'image', 'qty', 'price', 'total')
    search_fields = ('order__id', 'product__name', 'invoice_no', 'item')
    list_filter = ('order',)