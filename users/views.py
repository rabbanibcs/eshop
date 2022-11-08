from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Items
from users.utils import confirm_order,create_cart_while_logged_in
from users.models import Cart
from .forms import SignUpForm, CheckoutForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Address, Order, Wishlist
from django.urls import resolve
from django.http import Http404, HttpResponseRedirect

def check_out(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        print(form, 'form--')
        if form.is_valid:
            shipping_default = form.cleaned_data['shipping_default']
            if shipping_default == 'N':
                addresses = Address.objects.filter(user=request.user, default=True)
                addresses.update(default=False)
                for address in addresses:
                    address.save()
                # save new address as default
                shipping_address = form.cleaned_data.get('shipping_address')
                phone = form.cleaned_data.get('phone')
                zip = form.cleaned_data.get('zip')
                address = Address(
                    user=request.user,
                    shipping_address=shipping_address,
                    zip=zip,
                    phone=phone,
                )
                address.default = True
                address.save()
            else:
                address = Address.objects.filter(user=request.user, default=True).first()
                print(address)

            cart=Cart.objects.filter(user=request.user,ordered=False)

            order,created=Order.objects.get_or_create(user=request.user,ordered=False)
            order.items.set(cart)
            order.save()
            confirm_order(order)
            print(order,'order')
            return render(request, 'checkout.html', {'form': form, 'address': address})

    else:
        address = Address.objects.filter(user=request.user, default=True).first()
        print(address)

        form = CheckoutForm()
        return render(request, 'checkout.html', {'form': form, 'address': address})
    return render(request, 'checkout.html')


def sign_in(request):
    print(request.session.get('cart'), '---cart')
    cart = request.session.get('cart')
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=email, password=password)
            print('valid user')
            login(request, user)
            if cart:
                create_cart_while_logged_in(request, cart)
            return redirect('products')
        
        except:
            return redirect('signin')
        
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('signin')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. Now login..')
            return redirect('products')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# show all items in Cart.
def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, ordered=False)
        cart_total = cart.count()
        # print('cart', cart_total)
        total_price = 0
        for item in cart:
            total_price += item.get_final_price()

        context = {
            'cart_total': cart_total,
            'cart': cart,
            'total_price': total_price
        }
        return render(request, 'cart.html', context)
    else:
        cart = request.session.get('cart', {})
        dict = {}
        for item_key, qty in cart.items():
            dict[Items.objects.get(pk=int(item_key))] = qty
        context = {
            'cart_total': len(cart),
            'cart': dict
        }
        return render(request, '_cart.html', context)


# show all favorite items
@login_required
def favorite(request):
    print('wishlist-----------', request.method)
    liked = Wishlist.objects.filter(user=request.user)
    print('wish_list')
    if liked:
        for item in liked:
            print(item.item.name)
            context = {
                'objects': liked,
            }
    else:
        context = {
                'objects': {},
            }


    # print(request.path,' present path')
    # next = request.META.get('HTTP_REFERER', None)
    # print(next, 'previous path')
    # print(request.path)
    # match = resolve(next)
    # print(match)
    return render(request, 'wishlist.html', context)

