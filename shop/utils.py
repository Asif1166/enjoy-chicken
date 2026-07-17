from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from .models import CartOrder, CartOrderItems, CostSettings
from django.db.models import Sum
from datetime import datetime, time
from django.utils.timezone import make_aware
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from decimal import Decimal

def generate_pdf_report(start_date, end_date):
    # Convert string dates to datetime objects if needed
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Adjust start_date to start at 00:00 AM
    start_datetime = make_aware(datetime.combine(start_date, time.min))

    # Adjust end_date to end at 11:59 PM
    end_datetime = make_aware(datetime.combine(end_date, time.max))

    # Filter orders based on the adjusted date range and product status
    orders = CartOrder.objects.filter(
        order_date__range=[start_datetime, end_datetime],
        product_status__in=['accepted', 'delivered']  # Only these statuses
    ).select_related('shipping_address')  # Optimize query
    
    # Calculate total sales amount
    total_sales_amount = orders.aggregate(total_amount=Sum('price'))['total_amount'] or Decimal('0.00')
    
    # Calculate total tax amount from tax_amount field
    total_tax_amount = Decimal('0.00')
    for order in orders:
        if order.tax_amount:
            try:
                # Convert tax_amount to Decimal (it's a CharField)
                tax_value = Decimal(str(order.tax_amount))
                total_tax_amount += tax_value
            except (ValueError, TypeError):
                pass  # Skip if conversion fails
    
    # Calculate average order value
    order_count = orders.count()
    average_order_value = total_sales_amount / order_count if order_count > 0 else Decimal('0.00')
    
    # Prepare context for the PDF
    context = {
        'orders': orders,
        'total_sales_amount': total_sales_amount,
        'total_tax_amount': total_tax_amount,
        'average_order_value': average_order_value,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    
    # Render the HTML template with the context
    template = get_template('admin/report_template.html')
    html = template.render(context)
    
    # Generate PDF using xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{start_date.strftime("%Y-%m-%d")}_to_{end_date.strftime("%Y-%m-%d")}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response

def generate_invoice_pdf(order_id):
    # Get the order details
    order = CartOrder.objects.get(id=order_id)
    items = CartOrderItems.objects.filter(order=order)
    cost_settings = CostSettings.objects.last()
    
    # Assuming the CartOrder model has a related ShippingAddress model
    shipping_address = order.shipping_address

    # Calculate tax and totals using Decimal


    # Prepare context for the PDF
    context = {
        'order': {
            'created_at': order.order_date,
            'tax_amount': order.tax_amount,
            'price': order.price,
            'total_cost': order.total_cost,
            'order_id': order.id,
          
        },

        'items': items,
        'logo_url': '',
        'shipping_address': shipping_address,
        'cost_settings': cost_settings,
    }

    # Create PDF
    template = get_template('admin/invoice_template.html')
    html = template.render(context)
    
    # Configure PDF options for receipt-sized page
    pdf_options = {
        'page-width': '80mm',
        'page-height': '200mm',  # Adjust as needed for longer or shorter receipts
        'margin-top': '0.25in',
        'margin-right': '0.25in',
        'margin-bottom': '0.25in',
        'margin-left': '0.25in',
        'encoding': 'UTF-8',
        'no-outline': None,
        'quiet': None
    }

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
    
    pisa_status = pisa.CreatePDF(
        html, 
        dest=response,
        encoding='utf-8'
    )
    
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response
