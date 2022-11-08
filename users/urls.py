
from django.urls import path, include
from .views import *

urlpatterns = [
    path('checkout/', check_out, name='check_out'),
    path('signin/', sign_in, name='signin'),
    path('signout/', sign_out, name='signout'),
    path('signup/', sign_up, name='signup'),
    path('cart/', cart, name='cart'),
    path('favorite/', favorite, name='wishlist'),
    

]
