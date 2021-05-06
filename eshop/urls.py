from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from shop.views import ProductView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/',ProductView.as_view(),name='shop'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)