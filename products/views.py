from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Items
from users.models import Wishlist, Cart
from .utils import *
from django.http import HttpResponseRedirect

# Create your views here.



def all_products(request):
    items = Items.objects.all().order_by('?')
    contex = {
        'items': items
    }
    # print(request.META.get('HTTP_REFERER', '/'),'<--requested from that url')
    return render(request, 'products.html', contex)


def newest_products(request):
    items = Items.objects.all().order_by('-created_at')
    contex = {
        'items': items
    }
    return render(request, 'products.html', contex)


def low_price_products(request):
    items = Items.objects.all().order_by('price')
    contex = {
        'items': items
    }
    return render(request, 'products.html', contex)


def high_price_products(request):
    items = Items.objects.all().order_by('-price')
    contex = {
        'items': items
    }
    return render(request, 'products.html', contex)


def single_product(request, slug):
    product = Items.objects.get(slug=slug)
    like_products = Items.objects.filter(subcategory=product.subcategory).exclude(pk=product.id)
    try:
        wished = Wishlist.objects.get(user=request.user, item=product)
    except:
        wished = None
    try:
        in_cart = Cart.objects.get(user=request.user, item=product, ordered=False)
    except:
        in_cart = None
    return render(
        request,
        'single-product.html',
        {'product': product, 'like_products': like_products, 'wished': wished, 'in_cart': in_cart}
    )



# Remove an item to favorite.
@login_required
def remove_from_wishlist(request, pk):
    item = Items.objects.get(pk=pk)
    wished_item, created = Wishlist.objects.get_or_create(item=item, user=request.user)
    wished_item.delete()
    messages.info(request, "Item has been removed.")

    # keep user on the same page
    next = request.META.get('HTTP_REFERER', None) or '/'
    # print(next, 'previous path')
    response = HttpResponseRedirect(next)
    return response


# Add an item to favorite.
@login_required
def add_to_wishlist(request, pk):
    item = Items.objects.get(pk=pk)
    wished_item, created = Wishlist.objects.get_or_create(item=item, user=request.user)
    messages.info(request, "Item was added to your wishlist.")
    return redirect('single_product', slug=item.slug)


# reduce item quantity by one
def reduce_cart(request, pk):
    item = get_object_or_404(Items, pk=pk)
    if request.user.is_authenticated:
        item_in_cart = Cart.objects.get(user=request.user, item=item, ordered=False)
        if item_in_cart.quantity > 1:
            item_in_cart.quantity -= 1
            item_in_cart.save()
        else:
            remove_from_cart_for_authenticated_user(request, pk)
    else:
        cart = request.session.get('cart')
        if request.session['cart'][str(pk)] > 1:
            # Session is NOT modified so save it
            request.session['cart'][str(pk)] -= 1
            request.session.save()
        else:
            request.session['cart'].pop(str(pk))
            request.session.save()
    return redirect("cart")



# remove item from Cart.
def remove_from_cart(request, pk):
    if request.user.is_authenticated:
        print('remove_from_cart')
        remove_from_cart_for_authenticated_user(request, pk)
        return redirect("cart")
    else:
        request.session['cart'].pop(str(pk))
        request.session.save()
        return redirect("cart")


# Add a item to Cart.
def add_to_cart(request, pk):
    print('ad to cart-----------', request.method)

    if request.user.is_authenticated:
        item = add_to_cart_for_authenticated_user(request, pk)
        try:
            wish_item = Wishlist.objects.get(item=item, user=request.user)
            wish_item.delete()
        except:
            pass
        return redirect("cart")

    else:
        item = add_to_cart_for_anonymous_user(request, pk)
        # del request.session['cart']
        return redirect("cart")

















