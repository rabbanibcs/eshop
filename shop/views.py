from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.conf import settings
import os


from shop.models import Product, Category, Customer, Cart, Order


class ProductsView(View):

    def get(self, request):
        category = Category.objects.all()

        # search functionality. by product name.
        if request.GET.get('query'):
            query = request.GET.get('query')
            products = Product.objects.filter(name__startswith=query)
            if products:
                pass
            else:
                messages.warning(request, 'No product found.')
        else:
            products = Product.objects.all()
        context = {'products': products, 'category': category}
        return render(request, 'shop/shop.html', context)

    def post(self, request):

        # search for category
        if request.POST.get('category'):
            category_id = request.POST.get('category')
            products = Product.objects.filter(category_id=category_id)
            # product_id = Product.objects.filter(category_id=category_id)
            context = {'products': products}
            return render(request, 'shop/shop.html', context)

        # search for products the given category
        if request.POST.get('product_id'):
            product_id = request.POST.get('product_id')
            print('product_id', product_id)
            product = Product.objects.filter(id=product_id)
            stock = Product.objects.get(pk=product_id).stock
            context = {'stock': stock, 'products': product, 'id': product_id}
            return render(request, 'shop/shop.html', context)

        # take input from user and add to cart
        if request.POST.get('quantity'):
            product_id = request.POST.get('id')
            quantity = request.POST.get('quantity')
            stock = Product.objects.get(pk=product_id).stock

            if int(quantity) > stock:
                messages.error(request, 'Sorry, Quantity is more than Stock')
            else:
                self.add_to_cart(request, product_id, quantity)
            category = Category.objects.all()
            products = Product.objects.all()
            context = {'category': category, 'products': products}

            return render(request, 'shop/shop.html', context)

        # add to cart from product view
        if request.POST.get('product'):
            product_id = request.POST.get('product')
            self.add_to_cart(request, product_id)
            return redirect('shop')

    # add to cart functionality
    @staticmethod
    def add_to_cart(request, product_id, quantity='1'):
        pk = product_id
        q = int(quantity)
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(pk)
            if quantity:
                cart[pk] = (q + quantity)
            else:
                cart[pk] = q
        else:
            cart = {pk: q}
        request.session['cart'] = cart
        messages.success(request, 'Added to the Cart. ')


class CartView(View):
    # view of the cart
    def get(self, request):
        cart = request.session.get('cart')
        products = {}
        if cart:
            for product_id, quantity in cart.items():
                product = Product.objects.get(pk=product_id)
                products[product] = quantity

        context = {'products': products, }
        return render(request, 'shop/cart.html', context)

    # delete a product from cart
    def post(self, request):
        if request.POST.get('product'):
            pro_id = request.POST.get('product')
            del request.session['cart'][pro_id]
        request.session.save()
        cart = request.session.get('cart')
        products = {}
        for product_id, quantity in cart.items():
            product = Product.objects.get(pk=product_id)
            products[product] = quantity

        context = {'products': products, }
        return render(request, 'shop/cart.html', context)


class OrderView(View):
    def post(self, request):
        if request.POST.get('email'):
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            customer = Customer(name=name, phone=phone, email=email)
            customer.save()
            qrcode_path = customer.qrcode_create()
            customer.qrcode = qrcode_path
            customer.save()
            order = Order(customer=customer, )
            order.save()
            cart = request.session.get('cart')
            if cart:
                for product_id, quantity in cart.items():
                    cart = Cart(product_id=product_id, quantity=quantity, order=order, complete=True)
                    cart.save()
                del request.session['cart']
                request.session.save()
        cart = order.cart_set.all()
        context = {'cart': cart, 'order': order}
        return render(request, 'shop/order.html', context)

    def get(self, request):
        order = Order.objects.get(pk=24)
        cart = order.cart_set.all()
        context = {'cart': cart, 'order': order}
        return render(request, 'shop/order.html', context)


def order_pdf_view(request):
    order = Order.objects.get(pk=24)
    cart = order.cart_set.all()
    context = {'cart': cart, 'order': order}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template('shop/order.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path