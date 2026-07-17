from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list_view, name='products'),
    path('categories/', views.category_list_view, name='categories'),
    path('category/<str:cid>/', views.category_product_list_view, name='category_products'),
    path('supercategory/', views.super_category_product_list_view, name='super_category_product_list_view'),
    path('product-details/<pid>/', views.product_details_view, name='product_details'),
    path('search/', views.search_view, name='search'),
    
    
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/', views.view_cart, name='cart_view'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('update-cart/', views.update_form_cart, name='update-cart'),
    path('delete-from-cart/', views.delete_item_from_cart, name='delete_item_from_cart'),
    path('delete-from-wishlist/', views.delete_item_from_wishlist, name='delete_item_from_wishlist'),
    
    path('checkout/', views.checkout_view, name='checkout'),
    
    # path('payment/', views.payment_view, name='payment'),
    # path('payment-confirmation/', views.payment_confirmation_view, name='payment_confirmation'),

    
    path('order-complete/', views.order_complete_view, name='order_complete'),
    path('order-confirmation/', views.order_confirmation_view, name='order_confirmation'),

    path('dashboard/', views.customer_dashboard, name='dashboard'),
    path('dashboard/order/<int:id>', views.order_details, name='order_details'),
    path('track-order/', views.track_order, name='track_order'),
    path('order-track/', views.order_track, name='order_track'),

    path('invoice/download/<int:order_id>/', views.generate_invoice_pdf, name='invoice_download'),


    path('check-new-orders/', views.check_new_orders, name='check_new_orders'),

    path('fetch_notifications/', views.fetch_notifications, name='fetch_notifications'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('clear_notifications/', views.clear_notifications, name='clear_notifications'),  # New URL

    
]