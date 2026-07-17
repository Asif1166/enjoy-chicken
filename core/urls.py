
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('user/', include('authentication.urls')),
    path('', include('shop.urls')),
    path('', include('cms.urls')),
    path('custom-admin/', include('custom_admin.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404_view