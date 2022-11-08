from django.urls import path
from .views import *

urlpatterns = [
    path('products/', all_products, name='products'),
    path('newest/',newest_products, name='newest_products'),
    path('high-price/',high_price_products, name='high_price_products'),
    path('low-price/',low_price_products, name='low_price_products'),
    path('single/<slug:slug>/', single_product, name='single_product'),
    path('add-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('reduce-cart/<int:pk>/', reduce_cart, name='reduce_cart'),
    path('remove-cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('add-to-wishlist/<int:pk>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:pk>/', remove_from_wishlist, name='remove_from_wishlist'),


]