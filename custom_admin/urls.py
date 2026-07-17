from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('orders', views.orders, name='orders'),
    path('update-order-status/', views.update_order_status, name='update_order_status'),
    path('download-invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path('delete-sale/<int:order_id>/', views.delete_sale, name='delete_sale'),
    path('toggle-order-on-off-status/', views.toggle_order_on_off_status, name='toggle_order_on_off_status'),
    path('toggle-delivery-on-off-status/', views.toggle_delivery_on_off_status, name='toggle_delivery_on_off_status'),
    path('toggle-take-away-on-off-status/', views.toggle_take_away_on_off_status, name='toggle_take_away_on_off_status'),
    path('toggle-paid-status/<int:order_id>/', views.toggle_paid_status, name='toggle_paid_status'),

    path('admin/report/', views.report_view, name='generate_report'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    path('process_all_orders/', views.process_all_orders, name='process_all_orders'),
    path('fetch-orders-data/', views.fetch_orders_data, name='fetch_orders_data'),
    
    path('reservation-list/', views.reservation_list, name='reservation_list'),
    path('delete-reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('update-reservation-status/', views.update_reservation_status, name='update_reservation_status'),

    path('toggle-reservation-status/', views.toggle_reservation_status, name='toggle_reservation_status'),

]


