from django import template
from users.models import *


register = template.Library()

# total items in cart for authenticated user
@register.filter()
def total_items_in_cart(user):
    qs = Cart.objects.filter(user=user, ordered=False)
    if qs.exists():
        # print(qs[0].items.count(),' count')
        return qs.count()
    else:
        return 0
# total items in cart stored in sesssion for anonymous user
@register.filter()
def total_items_in_cart_(request):
    # print('user anonymous')
    cart=request.session.get('cart')
    if cart:
        # print(request.session['cart'])
        return len(cart)
    else:
        return 0

@register.filter()
def total_items_in_wishlist(user):
    # print(user,'user')
    if user.is_authenticated:
        # print('annonymous')
        qs = Wishlist.objects.filter(user=user)
        if qs.exists():
            # print(qs[0].items.count(),' count')
            return qs.count()
        else:
            return 0

@register.filter()
def total_price(item,qty):
    return item.discount_price*qty

@register.filter()
def amount_saved(item,qty=0):
    return item.price*qty-item.discount_price*qty
