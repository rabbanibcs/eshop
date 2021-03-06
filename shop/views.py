from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
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
            # get quantity if the product product is in the cart.
            quantity_in_cart = self.quantity_in_cart(request, product_id)
            quantity = int(quantity) + quantity_in_cart

            # check if quantity is more than stock then add to cart
            if int(quantity) > stock:
                if quantity_in_cart:
                    messages.error(request,
                                   f'Sorry, Quantity is more than Stock.\n You have already added {quantity_in_cart}')
                else:
                    messages.error(request, 'Sorry, Quantity is more than Stock, Try again.')
            else:
                self.add_to_cart(request, product_id, quantity)
            category = Category.objects.all()
            products = Product.objects.all()
            context = {'category': category, 'products': products}

            return render(request, 'shop/shop.html', context)

        # add to cart from product view
        if request.POST.get('product'):
            product_id = request.POST.get('product')
            stock = Product.objects.get(pk=product_id).stock
            # get quantity if the product product is in the cart.
            quantity = self.quantity_in_cart(request, product_id)
            # check if quantity is more than stock then add to cart
            if quantity:
                if quantity == stock:
                    messages.error(request, f'Sorry, You have already added {quantity}.\n But we have only {quantity} in '
                                            f'stock')
                else:
                    self.add_to_cart(request, product_id)
            else:
                self.add_to_cart(request, product_id)
            return redirect('shop')

    # returns quantity of that product, that is already in cart
    @staticmethod
    def quantity_in_cart(request, product_id):
        pk = product_id
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(pk)
            if quantity:
                return quantity
        return 0

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
    #  create customer,order and save cart, create QR code
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

    # view order
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        cart = order.cart_set.all()
        context = {'cart': cart, 'order': order}
        return render(request, 'shop/order.html', context)


# generate a pdf of Order,
def order_pdf_view(request, pk):
    order = Order.objects.get(pk=pk)
    cart = order.cart_set.all()
    context = {'cart': cart, 'order': order}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template('shop/order.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
