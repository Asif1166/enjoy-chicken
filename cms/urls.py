from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('photo-gallery/', views.photo_gallery, name='photo_gallery'),
    path('video-gallery/', views.video_gallery, name='video_gallery'),
    path('reservation/', views.reservation, name='reservation'),
    path('reservation/success/', views.reservation_success, name='reservation_success'),
    path('le_carte/', views.product, name='product'),
    path('track_order/', views.track_order, name='track_order'),
    path('get_menu_api/', views.get_menu_api, name='get_menu_api'),

]