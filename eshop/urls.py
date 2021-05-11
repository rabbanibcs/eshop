from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from shop.views import ProductsView,OrderView,CartView,order_pdf_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/',ProductsView.as_view(),name='shop'),
    path('order/', OrderView.as_view(),),
    path('order/<int:pk>', OrderView.as_view(), ),
    path('order/download/',order_pdf_view, ),
    path('cart/', CartView.as_view(), name='cart'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)